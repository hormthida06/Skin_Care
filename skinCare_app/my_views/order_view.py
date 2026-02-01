from django.shortcuts import render
from django.core.paginator import Paginator
from skinCare_app.models import Order
from django.db.models import Q


def order_list(request):
    orders = Order.objects.select_related("user").all()

    # Search
    name = request.GET.get("name")
    if name:
        orders = orders.filter(user__username__icontains=name)

    # Sorting
    sort = request.GET.get("sort")
    if sort == "az":
        orders = orders.order_by("user__username")
    elif sort == "za":
        orders = orders.order_by("-user__username")
    else:
        orders = orders.order_by("-order_id")

    paginator = Paginator(orders, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "table/order/list.html", {
        "page_obj": page_obj,
        "sort_option": sort,
        "search_name": name,
    })

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def order_delete(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    order.delete()
    messages.success(request, "Order deleted successfully!")
    return redirect("order_list")
