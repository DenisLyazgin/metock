from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.http import JsonResponse
from django.contrib.auth.models import User


def clogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('video_view')
        else:
            messages.error(request, "Неверные данные для входа")
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})  # <-- передаем form


def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('video_view')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})  # <-- передаем form



def clogout(request):
    logout(request)
    return redirect('login')

def check_username(request):
    username = request.GET.get('username', None)
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})
