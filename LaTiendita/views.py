from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from LaTiendita.Carrito import Carrito

# Create your views here.

def inicio(request):
    return render(request, 'public/inicio.html')

def correa(request):
    return render(request, 'public/correa.html')

def bandana(request):
    productos = Producto.objects.filter(stock__gt=0, categoria='bandana') 
    context = {
        'productos': productos,
    }

    return render(request, 'public/bandana.html', context)

def identificador(request):

    return render(request, 'public/identificador.html')

def descrip_carro(request):
    return render(request, 'public/descrip_carrito.html')

def lista_productos(request):
    productos = Producto.objects.all()  
    context = {
        'productos': productos,
    }
    return render(request, "carrito", context)

def agregar_producto(request, producto_id):
    v_carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    v_carrito.agregar(producto)
    return redirect("bandana")

def eliminar_producto(request, producto_id):
    v_carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    v_carrito.eliminar(producto)
    return redirect("bandana")

def restar_producto(request, producto_id):
    v_carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    v_carrito.restar(producto)
    return redirect("bandana")

def limpiar_carrito(request):
    v_carrito = Carrito(request)
    v_carrito.limpiar()
    return redirect("bandana")