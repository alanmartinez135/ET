from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Producto)
admin.site.register(DetalleCompra)
admin.site.register(Carrito)
admin.site.register(DetalleCarrito)