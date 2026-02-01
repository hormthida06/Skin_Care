from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from skinCare_app.models import Order, Payment, OrderItem


BOT_TOKEN = "8293252571:AAEPLExFsTh_HwtCjG5jnEFQ9Ge3dHIpgaE"
CHAT_ID = "@thida_channel"

def khqr_status(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id)
        payment = Payment.objects.filter(order=order).last()

        if payment and payment.status == "Paid":
            return JsonResponse({
                "status": "paid",
                "payment_id": payment.payment_id
            })

        return JsonResponse({"status": "pending"})

    except Order.DoesNotExist:
        return JsonResponse({"status": "not_found"})

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    requests.post(url, json=payload)

@csrf_exempt
def khqr_payment_callback(request):

    data = json.loads(request.body)

    order_id = data.get("order_id")
    transaction_id = data.get("transaction_id")
    amount = data.get("amount")

    order = Order.objects.get(order_id=order_id)

    payment = Payment.objects.filter(order=order).last()
    if payment:
        payment.status = "Paid"
        payment.transaction_id = transaction_id
        payment.paid_at = timezone.now()
        payment.save()

    order.payment_status = "Paid"
    order.save()
    send_telegram_order_paid(order)

    return JsonResponse({"status": "success"})

def send_telegram_order_paid(order):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    user = {
        "name": order.user.full_name,
        "email": order.user.email,
        "phone": order.user.phone,
        "address": order.shipping_address,
    }

    items = order.orderitem_set.all()
    subtotal = order.total_amount
    tax = subtotal * 0.10
    total = subtotal + tax

    message = (
        "<b>PAYMENT SUCCESS</b>\n\n"
        f"<b>Order ID:</b> {order.order_id}\n"
        f"<b>Name:</b> {user['name']}\n"
        f"<b>Email:</b> {user['email']}\n"
        f"<b>Phone:</b> {user['phone']}\n"
        f"<b>Address:</b> {user['address']}\n\n"
        "<b>Items:</b>\n"
    )

    for item in items:
        message += f"• {item.product.product_name} × {item.quantity}\n"

    message += (
        "\n <b>Payment Summary:</b>\n"
        f"Subtotal: ${subtotal:.2f}\n"
        f"Tax (10%): ${tax:.2f}\n"
        f"<b>Total:</b> ${total:.2f}\n"
        "\n Payment Method: KHQR\n"
        "Status: PAID "
    )

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    requests.post(url, json=payload)

def test_telegram(request):
    payload = {
        "chat_id": CHAT_ID,
        "text": "Hello, this is a test message!",
    }
    response = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json=payload)
    return JsonResponse({"status_code": response.status_code, "response": response.json()})

