from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

from skinCare_app.models import User, UserProfile

def dashboard(request):
    if request.session.get('role') != 'admin':
        messages.error(request, "Access denied.")
        return redirect('/')
    return render(request, 'table/dashboard_body.html')

# Register View
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

        # Create user
        user = User(user_name=username, email=email, role='customer')
        user.set_password(password)
        # For managed=False models, you must provide created_at manually
        from django.utils import timezone
        user.created_at = timezone.now()
        user.save()

        # Create profile
        UserProfile.objects.create(user=user)

        messages.success(request, "Registration successful. Please login.")
        return redirect('login')

    return render(request, 'pages/login.html')


# Login View
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                request.session['user_id'] = user.id
                request.session['user_name'] = user.user_name
                request.session['role'] = user.role

                if user.role == 'admin':
                    return redirect('dashboard')
                else:
                    return redirect('/')
            else:
                messages.error(request, "Invalid password.")
        except User.DoesNotExist:
            messages.error(request, "Email not found.")

        return redirect('login')

    return render(request, 'pages/login.html')


# Logout View
def logout_view(request):
    request.session.flush()
    return redirect('/')
