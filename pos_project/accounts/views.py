# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .models import Request

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
    return redirect('')


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
    requests_list = Request.objects.all().order_by('-date')  # latest first
    return render(request, 'Home/dashboard.html', {"requests": requests_list})


@login_required(login_url='login')
def request_detail(request, id):
    req = get_object_or_404(Request, id=id)
    return render(request, 'Home/request_detail.html', {'req': req})


@login_required(login_url='login')
def edit_request(request, id):
    req = get_object_or_404(Request, id=id)
    if request.method == 'POST':
        req.title = request.POST.get('title')
        req.status = request.POST.get('status')
        req.date = request.POST.get('date')
        req.description = request.POST.get('description')
        req.save()
        return redirect('dashboard')
    return render(request, 'Home/edit_request.html', {'req': req})


@login_required(login_url='login')
def delete_request(request, id):
    req = get_object_or_404(Request, id=id)
    if request.method == 'POST':
        req.delete()
        return redirect('dashboard')
    return render(request, 'Home/confirm_delete.html', {'req': req})

@login_required(login_url='login')
def add_request(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        status = request.POST.get('status')
        date = request.POST.get('date')
        description = request.POST.get('description')
        Request.objects.create(title=title, status=status, date=date, description=description)
        return redirect('dashboard')
    return render(request, 'Home/add_request.html')


def landing_page(request):
    return render(request, 'Home/landing.html')