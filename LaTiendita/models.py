from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete= models.CASCADE)
    run = models.IntegerField(verbose_name='run', unique=True)
    saldo = models.IntegerField(default=0)
    role = models.CharField(max_length=9, choices=settings.ROLES)
    def __str__(self):
        return f'{self.role}:  {self.user.username}'
    
class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre producto', max_length=50, blank=False, null=False)
    precio = models.IntegerField()
    descripcion = models.TextField()
    categoria = models.CharField(max_length=20, blank=False, null=False)
    stock = stock = models.IntegerField()
    imagen = models.ImageField('Imagen del producto', upload_to='LaTiendita/media/productos/', blank=True, null=True)

    def __str__(self):
        return f"Nombre producto : {self.nombre}"
  

class DetalleCompra(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_despacho = models.CharField(max_length=50)
    direccion_entrega = models.CharField(max_length=255, blank=True, null=True)  # Nuevo campo para la dirección de entrega
    fecha_compra = models.DateTimeField()
    usuario = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario} || Producto: {self.producto.nombre_plato} || Cantidad: {self.cantidad}"
    

class Carrito(models.Model):
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    
    def agregar(self, producto):
        detalle_carrito, created = DetalleCarrito.objects.get_or_create(carrito=self, defaults={
            'cantidad': 1,
            'total': producto.precio,
            'subtotal': producto.precio
        })
        if not created:
            detalle_carrito.cantidad += 1
            detalle_carrito.total += producto.precio
            detalle_carrito.subtotal += producto.precio
            detalle_carrito.save()
    def __str__(self):
        return f'Carrito de {self.usuario.username}'

class DetalleCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ManyToManyField(Producto)
    cantidad = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)  
    
    def __str__(self):
        return f'Detalle de {self.carrito.usuario.username}'
    