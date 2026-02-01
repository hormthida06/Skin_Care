# views.py
from django.shortcuts import render
from django.core.paginator import Paginator

from skinCare_app.models import User, UserProfile
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

def user_list(request):
    users = User.objects.all()

    # Search
    name = request.GET.get('name')
    if name and name != "None":
        users = users.filter(user_name__icontains=name)

    # Sorting
    sort = request.GET.get('sort')
    if sort == "az":
        users = users.order_by("user_name")
    elif sort == "za":
        users = users.order_by("-user_name")
    else:
        users = users.order_by("-id")

    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    users = User.objects.all()
    user_profilt = UserProfile.objects.all()

    return render(request, 'table/user/list.html', {
        'page_obj': page_obj,
        'sort_option': sort,
        'search_name': name
    })

def user_delete(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('user_list')