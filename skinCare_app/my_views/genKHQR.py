import requests
from django.http import JsonResponse
import json, uuid
from decimal import Decimal

from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from skinCare_app.models import Order, Payment
from decimal import Decimal, ROUND_HALF_UP

from bakong_khqr import KHQR
from django.conf import settings
from django.utils import timezone

from skinCare_app.my_views.Telegram_Notification_view import send_telegram_order_paid, test_telegram, \
    khqr_payment_callback

khqr = KHQR()


@csrf_exempt
def generate_khqr(request):
    order = get_object_or_404(Order, order_id=request.session["last_order_id"])

    subtotal = Decimal(order.total_amount)
    tax = subtotal * Decimal("0.10")
    delivery = Decimal("2.50")

    total_amount = (subtotal + tax + delivery).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    qr_string = khqr.create_qr(
        bank_account=settings.BAKONG_ID,
        merchant_name="Horm Thida",
        merchant_city="Phnom Penh",
        amount=float(total_amount),
        currency="USD",
        store_label="SkinCare Shop",
        phone_number="0976970127",
        bill_number=f"TRX-{uuid.uuid4().hex[:8]}",
        terminal_label="POS-01",
        static=False
    )

    import hashlib
    md5 = hashlib.md5(qr_string.encode()).hexdigest()

    request.session["order_md5"] = md5
    request.session["order_total"] = str(total_amount)

    return JsonResponse({
        "qrData": qr_string,
        "md5": md5,
        "total": str(total_amount)
    })

def check_transaction_status(request):
    md5 = request.GET.get("md5") or request.session.get("order_md5")

    if not md5:
        return JsonResponse({"paid": False, "error": "No MD5"})

    url = "https://api-bakong.nbc.gov.kh/v1/check_transaction_by_md5"
    headers = {
        "Authorization": f"Bearer {settings.BAKONG_TOKEN}",
        "Content-Type": "application/json"
    }

    res = requests.post(url, json={"md5": md5}, headers=headers, verify=False)
    result = res.json()

    print("BAKONG RESPONSE:", result)

    if result.get("responseCode") == 0 and result.get("data"):
        txn_id = result["data"].get("hash")  # Use hash
        order_id = request.session.get("last_order_id")

        if not order_id:
            return JsonResponse({"paid": False, "error": "No order in session"})

        try:
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            return JsonResponse({"paid": False, "error": "Order not found"})

        # Ensure total_amount exists
        if order.total_amount is None:
            return JsonResponse({"paid": False, "error": "Order total amount is missing"})

        # Check existing payment
        payment = Payment.objects.filter(order=order, payment_method="KHQR").first()

        if not payment:
            payment = Payment.objects.create(
                order=order,
                payment_method="KHQR",
                amount=order.total_amount * Decimal("1.1"),
                status="Success",
                transaction_id=txn_id,
                paid_at=timezone.now()
            )
            # Update order
            order.payment_status = "Paid"
            order.save()
            send_telegram_order_paid(order)
        return JsonResponse({"paid": True, "redirect": f"/payment/success/{payment.payment_id}"})

    return JsonResponse({"paid": False, "pending": True})

def khqr_status(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)

    payment = Payment.objects.filter(order=order, payment_method="KHQR").first()
    if payment:
        return JsonResponse({
            "status": "success",
            "payment_id": payment.payment_id
        })

    return JsonResponse({"status": "pending"})

@csrf_exempt
def khqr_webhook(request):
    data = json.loads(request.body)
    order_id = data["order_id"]
    status = data["status"]

    order = Order.objects.get(order_id=order_id)

    if status == "SUCCESS":
        Payment.objects.create(
            order=order,
            payment_method="KHQR",
            amount=order.total_amount * 1.1,
            status="Paid",
            transaction_id=data["txn_id"],
            paid_at=timezone.now()
        )
        order.payment_status = "Paid"
        order.save()

    return JsonResponse({"ok": True})

