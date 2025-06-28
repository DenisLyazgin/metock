from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RegisterForm


def clogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, "Неверные данные для входа")
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html')


def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('main')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html')


def clogout(request):
    logout(request)
    return redirect('login')
