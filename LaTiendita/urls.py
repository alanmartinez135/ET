from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('bandana/', views.bandana, name='bandana'),
    path('descrip-carrito/', views.descrip_carro, name='descrip_carrito'),
    path('agregar/<int:producto_id>/', views.agregar_producto, name='add'),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name='del'),
    path('restar/<int:producto_id>/', views.restar_producto, name='sub'),
    path('limpiar/', views.limpiar_carrito, name='cls'),
    path('pago/', views.pago, name='pago'),
    path('confirmacion/', views.confirmacion, name='confirmacion'),
]

