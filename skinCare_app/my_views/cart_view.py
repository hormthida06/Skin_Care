from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from skinCare_app.models import Cart, CartItem, Product

# -------------------- Helper function --------------------
def get_cart(user_id):
    cart, _ = Cart.objects.get_or_create(user_id=user_id)
    items = CartItem.objects.filter(cart=cart)
    total_items = sum(item.quantity for item in items)
    total_price = sum(item.subtotal for item in items)
    return cart, items, total_items, total_price

# -------------------- Cart page view --------------------
def cart_view(request):

    user_id = request.session.get("user_id")
    if not user_id:
        return render(request, "index.html", {"items": [], "total_items": 0, "total_price": 0})

    cart, items, total_items, total_price = get_cart(user_id)
    context = {
        "items": items,
        "total_items": total_items,
        "total_price": total_price,
    }
    return render(request, "index.html", context)

# -------------------- Add to cart --------------------
@csrf_exempt
def add_to_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get("product_id")
        user_id = request.session.get("user_id")

        if not user_id:
            return JsonResponse({"success": False, "message": "Login required"})

        try:
            # Fetch the product object
            product = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({"success": False, "message": "Product not found"})

        cart, _ = Cart.objects.get_or_create(user_id=user_id)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            item.quantity += 1
            item.save()
        else:
            item.quantity = 1
            item.save()

        # Recalculate totals
        items = CartItem.objects.filter(cart=cart)
        total_items = sum(i.quantity for i in items)
        total_price = sum(i.subtotal for i in items)

        return JsonResponse({
            "success": True,
            "total_items": total_items,
            "total_price": float(total_price),
            "item_quantity": item.quantity,
            "message": "Added to cart"
        })

# -------------------- Update cart item --------------------
@csrf_exempt
def update_cart_item(request):
    if request.method == "POST":
        data = json.loads(request.body)
        item_id = data["item_id"]
        quantity = int(data["quantity"])

        item = CartItem.objects.get(id=item_id)
        item.quantity = quantity
        item.save()

        return JsonResponse({
            "success": True,
            "subtotal": float(item.subtotal),
            "unit_price": float(item.product.price)
        })

# -------------------- Remove cart item --------------------
@csrf_exempt
def remove_cart_item(request, item_id):
    try:
        item = CartItem.objects.get(id=item_id)
        item.delete()
        return redirect("/")
    except CartItem.DoesNotExist:
        return redirect("/")


def some_page_view(request):
    user_id = request.session.get("user_id")
    cart_total_items = 0
    if user_id:
        _, _, cart_total_items, _ = get_cart(user_id)

    context = {
        "cart_total_items": cart_total_items,
    }
    return render(request, "index.html", context)

@property
def subtotal(self):
    return self.product.price * self.quantity

