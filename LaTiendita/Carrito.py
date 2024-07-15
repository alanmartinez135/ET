from .models import Carrito as CarritoModel, DetalleCarrito

class Carrito:
    def __init__(self, usuario):
        self.usuario = usuario
        self.carrito, created = CarritoModel.objects.get_or_create(usuario=self.usuario, activo=True)
    
    def agregar(self, producto):
        detalle_carrito, created = DetalleCarrito.objects.get_or_create(carrito=self.carrito, producto=producto, defaults={
            'cantidad': 1,
            'total': producto.precio,
            'subtotal': producto.precio
        })
        if not created:
            detalle_carrito.cantidad += 1
            detalle_carrito.total += producto.precio
            detalle_carrito.subtotal += producto.precio
            detalle_carrito.save()
    
    def eliminar(self, producto):
        try:
            detalle_carrito = DetalleCarrito.objects.get(carrito=self.carrito, producto=producto)
            if detalle_carrito.cantidad > 1:
                detalle_carrito.cantidad -= 1
                detalle_carrito.total -= producto.precio
                detalle_carrito.subtotal -= producto.precio
                detalle_carrito.save()
            else:
                detalle_carrito.delete()
        except DetalleCarrito.DoesNotExist:
            pass  # Producto no encontrado en el carrito

    def limpiar(self):
        DetalleCarrito.objects.filter(carrito=self.carrito).delete()
