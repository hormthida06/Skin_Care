from django.core.paginator import Paginator
from django.shortcuts import render
from skinCare_app.models import Product, Category, Concern, Cart, CartItem

def home(request):
    # ============ PRODUCTS ============
    products = Product.objects.all()

    # Filters
    skin = request.GET.get('skin')
    category_id = request.GET.get('category')
    brand = request.GET.get('brand')
    max_price = request.GET.get('price')
    concern_name = request.GET.get('concern')

    if skin:
        products = products.filter(skin_type=skin)
    if category_id:
        products = products.filter(category_id=category_id)
    if brand:
        products = products.filter(brand__icontains=brand)
    if max_price:
        products = products.filter(price__lte=max_price)
    if concern_name:
        products = products.filter(concerns__name__iexact=concern_name)

    products = products.order_by('-created_at')

    paginator = Paginator(products.distinct(), 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    brands = (
        Product.objects
        .exclude(brand__isnull=True)
        .exclude(brand__exact='')
        .values_list('brand', flat=True)
        .distinct()
        .order_by('brand')
    )

    categories = Category.objects.all()
    concerns = Concern.objects.all()

    # ============ CART ============
    cart_items = []
    cart_total_items = 0
    cart_total_price = 0
    user_id = request.session.get('user_id')

    if user_id:
        cart = Cart.objects.filter(user_id=user_id).first()
        if cart:
            cart_items = CartItem.objects.filter(cart=cart)

            cart_total_items = sum(item.quantity for item in cart_items)

            cart_total_price = sum(item.subtotal for item in cart_items)

    return render(request, "index.html", {
        "page_obj": page_obj,
        "categories": categories,
        "concerns": concerns,
        "brands": brands,
        "cart_items": cart_items,
        "cart_total_items": cart_total_items,
        "cart_total_price": cart_total_price,
    })
