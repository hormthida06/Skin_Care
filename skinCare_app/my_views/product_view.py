from decimal import Decimal
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils import timezone
from skinCare_app.models import Product, Concern, Category

# -------------------------------
# List Products
# -------------------------------
def product_list(request):
    products_qs = Product.objects.all()

    # Search
    search_name = request.GET.get('name')
    if search_name:
        products_qs = products_qs.filter(product_name__icontains=search_name)

    # Sorting
    sort_option = request.GET.get('sort')
    if sort_option == 'low_to_high':
        products_qs = products_qs.order_by('price')
    elif sort_option == 'high_to_low':
        products_qs = products_qs.order_by('-price')
    else:
        products_qs = products_qs.order_by('-created_at')

    # Pagination
    paginator = Paginator(products_qs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "table/product/list.html", {
        "page_obj": page_obj,
        "sort_option": sort_option,
        "search_name": search_name,
    })


# -------------------------------
# Create Product
# -------------------------------
def create_product(request):
    categories = Category.objects.all()
    concerns = Concern.objects.all()

    if request.method == "POST":
        product_data = request.POST
        selected_concerns = request.POST.getlist('concerns')

        try:
            category_id = product_data.get('category_id')
            category = get_object_or_404(Category, pk=category_id) if category_id else None

            product = Product(
                product_name=product_data.get('product_name'),
                brand=product_data.get('brand'),
                skin_type=product_data.get('skin_type'),
                description=product_data.get('description'),
                ingredients=product_data.get('ingredients'),
                using=product_data.get('using'),
                price=Decimal(product_data.get('price', 0)),
                stock=int(product_data.get('stock', 0)),
                category=category,
                created_at=timezone.now(),
            )

            if request.FILES.get('image'):
                uploaded_file = request.FILES['image']
                fs = FileSystemStorage(location='media/')
                filename = fs.save(uploaded_file.name, uploaded_file)
                product.image_url = filename

            product.full_clean()
            product.save()

            # Save concerns
            for c_name in selected_concerns:
                concern, _ = Concern.objects.get_or_create(name=c_name)
                product.concerns.add(concern)

            messages.success(request, "Product created successfully")
            return redirect('product_list')

        except Exception as e:
            messages.error(request, f"Error: {e}")

    return render(request, "table/product/create.html", {
        "categories": categories,
        "concerns": concerns,
        "selected_concerns": [],
    })


# -------------------------------
# Edit Product
# -------------------------------
def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    skin_types = ["All", "Dry", "Oily", "Sensitive", "Combination"]
    concerns = Concern.objects.all()
    categories = Category.objects.all()
    product_concern_ids = list(product.concerns.values_list('id', flat=True))

    return render(request, "table/product/edit.html", {
        "product": product,
        "skin_types": skin_types,
        "concerns": concerns,
        "categories": categories,
        "product_concern_ids": product_concern_ids,
    })


# -------------------------------
# Update Product
# -------------------------------
def update_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        product.product_name = request.POST.get('product_name')
        product.brand = request.POST.get('brand')
        product.skin_type = request.POST.get('skin_type')
        product.description = request.POST.get('description')
        product.ingredients = request.POST.get('ingredients')
        product.using = request.POST.get('using')
        product.price = Decimal(request.POST.get('price', 0))
        product.stock = int(request.POST.get('stock', 0))

        category_id = request.POST.get('category_id')
        if category_id:
            product.category_id = category_id

        if request.FILES.get('image'):
            uploaded_file = request.FILES['image']
            fs = FileSystemStorage(location='media/')
            filename = fs.save(uploaded_file.name, uploaded_file)
            product.image_url = filename

        # Update concerns
        selected_concerns = request.POST.getlist('concerns')
        product.concerns.clear()
        for c_name in selected_concerns:
            concern, _ = Concern.objects.get_or_create(name=c_name)
            product.concerns.add(concern)

        try:
            product.full_clean()
            product.save()
            messages.success(request, "Product updated successfully")
        except ValidationError as e:
            messages.error(request, f"Error: {e}")
            return redirect('product_edit', product_id=product.product_id)

        return redirect('product_list')

    # GET request fallback
    return redirect('product_edit', product_id=product.product_id)


# -------------------------------
# Delete Product
# -------------------------------
def delete_product(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        product.delete()
        messages.success(request, "Product deleted successfully")
    except ObjectDoesNotExist:
        messages.error(request, "Product not found")
    return redirect('product_list')
