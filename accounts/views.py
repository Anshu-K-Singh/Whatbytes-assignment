from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from .forms import RegisterForm, LoginForm, ChangePasswordForm


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        errors = []
        if not username:
            errors.append('Username is required.')
        if not email:
            errors.append('Email is required.')
        if not password1:
            errors.append('Password is required.')
        if not password2:
            errors.append('Confirm password is required.')

        if User.objects.filter(username=username).exists():
            errors.append('Username already exists.')

        if User.objects.filter(email=email).exists():
            errors.append('Email already in use.')

        if password1 != password2:
            errors.append('Passwords do not match.')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'accounts/signup.html', {
                'form': RegisterForm(initial={
                    'username': username, 
                    'email': email
                })
            })

        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        errors = []
        if not username:
            errors.append('Username is required.')
        if not password:
            errors.append('Password is required.')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'accounts/login.html', {
                'form': LoginForm(initial={'username': username})
            })

        user = authenticate(username=username, password=password)
        
        if user is None:
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials.')
            return render(request, 'accounts/login.html', {
                'form': LoginForm(initial={'username': username})
            })
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
@never_cache
def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'accounts/dashboard.html')

@login_required
@never_cache
def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'accounts/profile.html')

@login_required
@never_cache
def change_password_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password1 = request.POST.get('new_password1', '')
        new_password2 = request.POST.get('new_password2', '')

        errors = []
        if not old_password:
            errors.append('Current password is required.')
        if not new_password1:
            errors.append('New password is required.')
        if not new_password2:
            errors.append('Confirm new password is required.')

        if not request.user.check_password(old_password):
            errors.append('Current password is incorrect.')

        if new_password1 != new_password2:
            errors.append('New passwords do not match.')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'accounts/password_change.html', {
                'form': ChangePasswordForm(request.user)
            })

        request.user.set_password(new_password1)
        request.user.save()
        messages.success(request, 'Password changed successfully.')
        return redirect('login')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'accounts/password_change.html', {'form': form})
