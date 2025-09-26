# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Registration successful. You can log in now.")
            return redirect('login')

    return render(request, 'accounts/register.html')


@login_required(login_url='login')
def home_view(request):
    return render(request, 'Home/home.html')


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})


@login_required(login_url='login')
def dashboard_view(request):
    # 📊 Temporary data (User Story 1)
    requests_list = [
        {"id": 1, "title": "Password Reset", "status": "Pending", "date": "2025-10-07"},
        {"id": 2, "title": "Course Enrollment Issue", "status": "Approved", "date": "2025-10-06"},
        {"id": 3, "title": "Schedule Change", "status": "Cancelled", "date": "2025-10-05"},
    ]
    return render(request, 'Home/dashboard.html', {"requests": requests_list})


@login_required(login_url='login')
def request_detail(request, id):
    # temp nga data sa details
    requests_list = [
        {"id": 1, "title": "Password Reset", "status": "Pending", "date": "2025-10-07", "description": "User requested a password reset due to forgotten credentials."},
        {"id": 2, "title": "Course Enrollment Issue", "status": "Approved", "date": "2025-10-06", "description": "Issue with enrolling in CS101 course has been resolved."},
        {"id": 3, "title": "Schedule Change", "status": "Cancelled", "date": "2025-10-05", "description": "Requested schedule change was cancelled by the admin."},
    ]

    req = next((r for r in requests_list if r["id"] == id), None)

    if not req:
        return render(request, 'Home/request_detail.html', {"error_message": "Request not found."})

    return render(request, 'Home/request_detail.html', {'req': req})
