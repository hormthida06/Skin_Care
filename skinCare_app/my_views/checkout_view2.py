from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

BOT_TOKEN = "8293252571:AAEPLExFsTh_HwtCjG5jnEFQ9Ge3dHIpgaE"
CHAT_ID = "@thida_channel"

@csrf_exempt
def checkout_process(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=405)

    data = json.loads(request.body)

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = json.loads(request.body.decode("utf-8"))
    user = data.get("user", {})
    items = data.get("items", [])
    total = data.get("total", 0)

    message = (
        "🛒 <b>NEW ORDER</b>\n\n"
        f"👤 <b>Name:</b> {user.get('name', '-')}\n"
        f"📧 <b>Email:</b> {user.get('email', '-')}\n"
        f"📞 <b>Phone:</b> {user.get('phone', '-')}\n"
        f"🏠 <b>Address:</b> {user.get('address', '-')}\n\n"
        "📦 <b>Items:</b>\n"
    )

    if items:
        for item in items:
            message += f"• {item.get('name', 'Unknown')} × {item.get('qty', 0)}\n"
    else:
        message += "• No items\n"

    message += f"\n💰 <b>Total:</b> {total}"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    requests.post(url, json=payload)
    return JsonResponse({"message": "Sent"})

from django.http import JsonResponse
import json, uuid
from bakong_khqr import KHQR

from django.shortcuts import get_object_or_404

from skinCare_app.models import Order, Payment

khqr = KHQR()

def generate_khqr(request):  # <-- must have request
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "POST required"}, status=405)

    try:
        data = json.loads(request.body)
        amount = float(data.get("amount", 0))
    except (ValueError, KeyError):
        return JsonResponse({"success": False, "message": "Invalid data"}, status=400)

    bill_number = f"TRX-{uuid.uuid4().hex[:8]}"

    qr = khqr.create_qr(
        bank_account='thida_horm@aclb',
        merchant_name='Horm Thida',
        merchant_city='Phnom Penh',
        # amount=round(amount, 2),
        amount=0.01,
        currency='USD',
        store_label='SkinCare Shop',
        phone_number='0976970127',
        bill_number=bill_number,
        terminal_label='POS-01',
        static=False
    )

    if isinstance(qr, dict):
        qr = qr.get("qr") or qr.get("payload") or str(qr)

    return JsonResponse({"qrData": qr})

def khqr_status(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)

    # Check if payment already exists
    payment = Payment.objects.filter(order=order, payment_method="KHQR").first()
    if payment:
        return JsonResponse({
            "status": "success",
            "payment_id": payment.payment_id
        })

    # Optionally: integrate KHQR API to verify if order is paid
    # If paid, create payment record
    # Example pseudo-code:
    '''
    khqr_paid = khqr_api_check(order_id)
    if khqr_paid:
        payment = Payment.objects.create(
            order=order,
            payment_method="KHQR",
            amount=order.total_amount,
            status="Success",
            transaction_id=f"TXN{order.order_id}{timezone.now().strftime('%Y%m%d%H%M%S')}",
            paid_at=timezone.now()
        )
        order.payment_status = "Paid"
        order.save()
        return JsonResponse({"status":"success", "payment_id": payment.payment_id})
    '''

    # If not yet paid
    return JsonResponse({"status": "pending"})