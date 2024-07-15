from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from LaTiendita.Carrito import Carrito
from django.utils import timezone
from django.db import transaction
from .decorators import role_required
from .Carrito import Carrito, DetalleCarrito
from .models import Producto, Carrito, UserProfile

# Create your views here.

def inicio(request):
    return render(request, 'public/inicio.html')

def bandana(request):
    productos = Producto.objects.filter(stock__gt=0, categoria='bandana') 
    context = {
        'productos': productos,
    }

    return render(request, 'public/bandana.html', context)

def registro(request):
    if request.method == 'POST':
        us = request.POST.get('InputUsuario')
        correo = request.POST.get('InputEmail1')
        run = request.POST.get('run')
        contrasenia = request.POST.get('InputPassword1')
        role = 'cliente'

        if User.objects.filter(username=us).exists():
            messages.error(request, 'El usuario ya está en uso')
            return render(request, 'auth/registro.html')

        if User.objects.filter(email=correo).exists():
            messages.error(request, 'El correo ya está en uso')
            return render(request, 'auth/registro.html')

        if User.objects.filter(id=run).exists():
            messages.error(request, 'El rut ya está en uso')
            return render(request, 'auth/registro.html')

        if not us:
            messages.error(request, 'El nombre de usuario es obligatorio')
            return render(request, 'auth/registro.html')

        user = User.objects.create_user(username=us, email=correo, password=contrasenia)
        UserProfile.objects.create(user=user, run=run, role=role)
        return redirect('inicio')

    return render(request, 'auth/registro.html')

@login_required
@role_required('admin', 'cliente')
def logout_view(request):
    auth_logout(request)
    return redirect('inicio')

def iniciar_sesion(request):
    error_message = None
    if request.method == 'POST':
        usuario = request.POST['InputUsuario']
        contrasenia = request.POST['InputPassword1']
        user = authenticate(request, username=usuario, password=contrasenia)
        if user is not None:
            profile = UserProfile.objects.get(user=user)
            request.session['perfil'] = profile.role
            auth_login(request, user)
            return redirect('inicio')
        else:
            error_message = 'Usuario o contraseña incorrectos, intente de nuevo.'
    return render(request, 'auth/iniciar_sesion.html', {'error_message': error_message})

def carro(request):
    perfil = request.session.get('perfil')
    productos = Producto.objects.filter(stock__gt=0)

    user_profile = None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = None

    context = {
        'perfil': perfil,
        'productos': productos,
        'user_profile': user_profile
    }
    return render(request, "public/carrito.html",context)

def descrip_carro(request):
    return render(request, 'public/descrip_carrito.html')

def lista_productos(request):
    productos = Producto.objects.all()  
    context = {
        'productos': productos,
    }
    return render(request, "carrito", context)


def agregar_producto(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    
    if 'carrito' not in request.session:
        request.session['carrito'] = {}
    
    carrito = request.session['carrito']
    
    if producto_id in carrito:
        carrito[producto_id]['cantidad'] += 1
        carrito[producto_id]['subtotal'] += producto.precio
    else:
        carrito[producto_id] = {
            'producto_id': producto_id,
            'nombre': producto.nombre,
            'precio': producto.precio,
            'cantidad': 1,
            'subtotal': producto.precio,
        }
    
    request.session.modified = True
    
    return redirect("bandana")

def eliminar_producto(request, producto_id):
    if 'carrito' in request.session:
        carrito = request.session['carrito']
        if producto_id in carrito:
            del carrito[producto_id]
            request.session.modified = True
    
    return redirect("bandana")

def restar_producto(request, producto_id):
    if 'carrito' in request.session:
        carrito = request.session['carrito']
        if producto_id in carrito:
            if carrito[producto_id]['cantidad'] > 1:
                carrito[producto_id]['cantidad'] -= 1
                carrito[producto_id]['subtotal'] -= carrito[producto_id]['precio']
            else:
                del carrito[producto_id]
            
            request.session.modified = True
    
    return redirect("bandana")

def limpiar_carrito(request):
    if 'carrito' in request.session:
        del request.session['carrito']
    return redirect("bandana")


@transaction.atomic
def pago(request):
    carrito = request.session.get('carrito', {})
    
    if not carrito:  # Verificar si el carrito está vacío
        return render(request, 'public/descrip_carrito.html', {'error': 'No existen productos en el carrito.'})
    
    if request.method == "POST":
        # Procesar la selección de despacho y método de pago
        despacho = request.POST.get('despacho', '')
        metodo_pago = request.POST.get('metodo_pago', '')
        
        # Validar dirección si se selecciona despacho a domicilio
        if despacho == 'domicilio':
            direccion = request.POST.get('direccion', '')
            if not direccion:
                messages.error(request, 'Debes ingresar una dirección para el despacho a domicilio.')
                return redirect('pago')
        else:
            direccion = None
        
        # Verificar si el usuario está autenticado
        if not request.user.is_authenticated:
            messages.warning(request, 'Debes iniciar sesión para realizar una compra.')
            return redirect('iniciar_sesion')  # Redirigir a la página de inicio de sesión
        
        # Obtener el UserProfile asociado al usuario actual
        try:
            user_profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            messages.error(request, 'Debes iniciar sesión antes de comprar.')
            return redirect('iniciar_sesion')  # O redirigir a la página de inicio si UserProfile no existe
        
        try:
            with transaction.atomic():
                # Guardar los detalles de la compra y actualizar el stock
                for key, value in carrito.items():
                    producto = Producto.objects.get(id=value['producto_id'])
                    cantidad_comprada = value['cantidad']
                    precio_total = value['acumulado']
                    
                    # Validar si la cantidad deseada supera el stock disponible
                    if cantidad_comprada > producto.stock:
                        messages.error(request, f'El producto "{producto.nombre_plato}" no tiene suficiente stock disponible.')
                        return redirect('descrip_carrito')  # O redirigir a la página del carrito
                    
                    # Crear el detalle de la compra
                    DetalleCompra.objects.create(
                        producto=producto,
                        cantidad=cantidad_comprada,
                        precio_total=precio_total,
                        tipo_despacho=despacho,
                        direccion_entrega=direccion,
                        fecha_compra=timezone.now(),
                        usuario=user_profile
                    )
                    
                    # Actualizar el stock del producto
                    producto.stock -= cantidad_comprada
                    producto.save()
                
                # Limpiar el carrito después de la compra
                del request.session['descrip_carrito']
                request.session.modified = True
                
                return redirect('inicio')  # Redirigir a la página de inicio después de la compra
        
        except Producto.DoesNotExist:
            messages.error(request, 'Uno o más productos no existen en nuestro inventario.')
            return redirect('descrip_carrito')  # O redirigir a la página del carrito
        
        except Exception as e:
            messages.error(request, f'Ocurrió un error al procesar tu compra: {str(e)}')
            return redirect('descrip_carrito')  # O redirigir a la página del carrito

    perfil = request.session.get('perfil')
    productos = Producto.objects.filter(stock__gt=0)
    user_profile = None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = None

    context = {
        'perfil': perfil,
        'productos': productos,
        'user_profile': user_profile
    }
        
    return render(request, 'public/pago.html', context)

def confirmacion(request):
    perfil = request.session.get('perfil')


    productos = Producto.objects.filter(stock__gt=0)

    user_profile = None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = None

    context = {
        'perfil': perfil,
        'productos': productos,
        'user_profile': user_profile
    }

    return render(request, 'public/confirmacion.html',context )