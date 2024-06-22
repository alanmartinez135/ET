from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.contrib import messages
from .models import UserProfile, PlatoProveedor
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def inicio(request):
    return render(request, 'public/inicio.html')

def correa(request):
    return render(request, 'public/correa.html')

def bandana(request):
    return render(request, 'public/bandana.html')