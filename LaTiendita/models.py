from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

# Create your models here.

class Producto(models.Model):
    nombre = models.CharField('Nombre producto', max_length=50, blank=False, null=False)
    precio = models.IntegerField()
    descripcion = models.TextField()
    categoria = models.CharField(max_length=20, blank=False, null=False)
    stock = stock = models.IntegerField()
    imagen = models.ImageField('Imagen del producto', upload_to='LaTiendita/media/productos/', blank=True, null=True)

    def __str__(self):
        return f"Nombre producto : {self.nombre}"
    
class Cliente(models.Model):
    nombre = models.CharField('Nombre cliente', max_length=50, blank=False, null=False)
    suscripcion = models.BooleanField('Suscripcion', default=True, blank=False, null=False)
    correo = models.EmailField('Correo', max_length=50, blank=False, null=False)

    def __str__(self):
        return f"Nombre cliente : {self.nombre}"
    
class Carrito(models.Model):
    cliente = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f'Carrito de {self.cliente.username}'