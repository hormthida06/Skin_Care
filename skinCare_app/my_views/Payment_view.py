
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone

from skinCare_app.models import Order, Payment, OrderItem
from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q

from decimal import Decimal

from skinCare_app.my_views.Telegram_Notification_view import send_telegram_order_paid, khqr_payment_callback


def payment(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    order_id = request.session.get("last_order_id")
    if not order_id:
        return redirect("checkout")

    order = get_object_or_404(Order, order_id=order_id, user__id=user_id)

    order_items = order.items.all()

    tax = order.total_amount * Decimal("0.10")
    delivery = Decimal("2.50")
    total_amount = order.total_amount + tax + delivery

    return render(request, "pages/payment.html", {
        "order": order,
        "order_items": order_items,
        "tax": tax,
        "delivery": delivery,
        "total_amount": total_amount,
    })

def process_payment(request):
    if request.method != "POST":
        return redirect("checkout")

    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    order_id = request.POST.get("order_id")
    order = get_object_or_404(Order, order_id=order_id, user_id=user_id)

    payment_method = request.POST.get("payment_method")
    if not payment_method:
        return redirect("payment")

    payment = Payment.objects.create(
        order=order,
        payment_method=payment_method,
        amount=order.total_amount,
        status="Success",
        transaction_id=f"TXN{order.order_id}{timezone.now().strftime('%Y%m%d%H%M%S')}",
        paid_at=timezone.now()
    )

    order.payment_status = "Paid"
    order.save()

    return redirect("payment_success", payment_id=payment.payment_id)

def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, payment_id=payment_id)
    order = payment.order
    profile = getattr(order.user, 'userprofile', None)

    return render(request, "pages/payment_success.html", {
        "payment": payment,
        "order": order,
        "profile": profile
    })


# def success(request):
#     return render(request, "pages/payment_success.html")

def check_payment(request, order_id):
    order = Order.objects.get(order_id=order_id)
    payment = Payment.objects.filter(order=order, status="Success").first()

    if payment:
        return JsonResponse({"paid": True, "payment_id": payment.payment_id})

    return JsonResponse({"paid": False})



def payment_list(request):
    payments = Payment.objects.select_related("order").all()

    #  Search by order ID or transaction_id
    search = request.GET.get("search")
    if search:
        payments = payments.filter(
            Q(order__order_id__icontains=search) |
            Q(transaction_id__icontains=search)
        )

    #  Sort
    sort = request.GET.get("sort")
    if sort == "amount_asc":
        payments = payments.order_by("amount")
    elif sort == "amount_desc":
        payments = payments.order_by("-amount")
    elif sort == "status":
        payments = payments.order_by("status")
    else:
        payments = payments.order_by("-payment_id")  # latest first

    #  Pagination (10 per page)
    paginator = Paginator(payments, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "table/payment/list.html", {
        "page_obj": page_obj,
        "search": search,
        "sort_option": sort,
    })

def payment_delete(request, id):
    payment = get_object_or_404(Payment, id=id)
    payment.delete()
    payment.success(request, 'User deleted successfully.')
    return redirect('payment_list')