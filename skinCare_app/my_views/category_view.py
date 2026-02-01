from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from django.contrib import messages

from skinCare_app.models import Category


def category_list(request):
    categories = Category.objects.all()

    # Search
    name = request.GET.get("name")
    if name:
        categories = categories.filter(category_name__icontains=name)

    # Sort
    sort = request.GET.get("sort")
    if sort == "az":
        categories = categories.order_by("category_name")
    elif sort == "za":
        categories = categories.order_by("-category_name")
    else:
        categories = categories.order_by("-category_id")

    # Pagination
    paginator = Paginator(categories, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "table/category/list.html", {
        "page_obj": page_obj,
        "search_name": name,
        "sort_option": sort,
    })

def category_delete(request, category_id):
    category = get_object_or_404(Category, category_id=category_id)
    category.delete()
    messages.success(request, "Category deleted successfully!")
    return redirect("category_list")

def category_create(request):
    if request.method == "POST":
        name = request.POST.get("category_name")
        description = request.POST.get("description")

        Category.objects.create(
            category_name=name,
            description=description
        )

        messages.success(request, "Category created successfully!")
        return redirect("category_list")

    return render(request, "table/category/create.html")

def category_edit(request, category_id):
    category = get_object_or_404(Category, category_id=category_id)

    if request.method == "POST":
        category.category_name = request.POST.get("category_name")
        category.description = request.POST.get("description")
        category.save()

        messages.success(request, "Category updated successfully!")
        return redirect("category_list")

    return render(request, "table/category/edit.html", {"category": category})

def category_update(request, category_id):
    category = get_object_or_404(Category, category_id=category_id)

    if request.method == "POST":
        category.category_name = request.POST.get("category_name")
        category.description = request.POST.get("description")
        category.save()

        messages.success(request, "Category updated successfully!")
        return redirect("category_list")

    return render(request, "table/category/edit.html", {"category": category})
