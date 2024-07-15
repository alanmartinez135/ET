from .models import Carrito

def total_carrito(request):
    total = 0
    if 'carrito' in request.session:
        carrito = request.session['carrito']
        for item in carrito.values():
            total += item.get('subtotal', 0)
    
    return {'total_carrito': total}
