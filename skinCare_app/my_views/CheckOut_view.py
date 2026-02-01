
from decimal import Decimal
import json
from django.shortcuts import render, redirect, get_object_or_404
from skinCare_app.models import User, UserProfile, CartItem, Product, Order, OrderItem

def detail(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return render(request, "pages/personal_detail.html", {
            "username": "",
            "email": "",
            "phone": "",
            "address": "",
            "cart_items": [],
            "cart_total_items": 0,
            "cart_total_price": 0,
            "selected_items_json": "{}",
        })

    user = get_object_or_404(User, pk=user_id)
    cart_items = CartItem.objects.filter(cart__user=user)

    cart_total_items = sum(item.quantity for item in cart_items)
    cart_total_price = sum(item.subtotal for item in cart_items)

    # Prepare cart data for frontend JS
    selected_items_dict = {str(item.id): item.quantity for item in cart_items}
    selected_items_json = json.dumps(selected_items_dict)

    if request.method == "POST":
        selected_items_json_post = request.POST.get("selected_items")
        if not selected_items_json_post:
            return redirect("detail")

        selected_items = json.loads(selected_items_json_post)

        total_amount = Decimal("0.00")

        # Create order
        order = Order.objects.create(
            user=user,
            total_amount=Decimal("0.00"),
            payment_status="Pending"
        )

        # Create order items
        for product_id, quantity in selected_items.items():
            product = get_object_or_404(Product, pk=int(product_id))
            quantity = int(quantity)
            subtotal = product.price * quantity
            total_amount += subtotal

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                subtotal=subtotal
            )

        # Update total
        order.total_amount = total_amount
        order.save()

        # Clear cart after checkout
        CartItem.objects.filter(cart__user=user).delete()

        request.session["last_order_id"] = order.order_id
        return redirect("payment")

    # Load user profile if exists
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None

    return render(request, "pages/personal_detail.html", {
        "username": user.user_name,
        "email": user.email,
        "phone": profile.phone if profile else "",
        "address": profile.address if profile else "",
        "cart_items": cart_items,
        "cart_total_items": cart_total_items,
        "cart_total_price": cart_total_price,
        "selected_items_json": selected_items_json
    })

def save_checkout(request):
    if request.method != "POST":
        return redirect("checkout")

    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    user = get_object_or_404(User, pk=user_id)

    # get selected items from hidden input
    selected_items_json = request.POST.get("selected_items")
    print("DEBUG selected_items_json:", selected_items_json)

    if not selected_items_json:
        print("Cart is empty")
        return redirect("checkout")

    selected_items = json.loads(selected_items_json)

    # Create order
    order = Order.objects.create(
        user=user,
        total_amount=Decimal("0.00"),
        payment_status="Pending"
    )

    total_amount = Decimal("0.00")

    for cart_item_id, quantity in selected_items.items():
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        subtotal = cart_item.product.price * int(quantity)
        total_amount += subtotal

        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=int(quantity),
            subtotal=subtotal
        )

    order.total_amount = total_amount
    order.save()

    CartItem.objects.filter(cart__user=user).delete()

    request.session["last_order_id"] = order.order_id
    return redirect("payment")

