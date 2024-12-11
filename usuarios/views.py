from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout



def index(request):
    return render(request, 'usuarios/index.html')


def profile(request):
    return render(request, 'usuarios/profile.html')


def user_register(request):
    return render(request, 'usuarios/form.html')

def user_login(request):
    return render(request, 'usuarios/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')


def edit_profile(request):
    return render(request, 'usuarios/form.html')


def delete_profile(request):
    # delete user
    return redirect('login')
