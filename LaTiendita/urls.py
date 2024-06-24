from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name = 'inicio'),
    path('correa/', views.correa, name = 'correa'),
    path('bandana/', views.bandana, name = 'bandana'),
    path('identificador/', views.identificador, name = 'identificador'),
    path('descrip-carrito/', views.descrip_carro, name='descrip-carrito'),
    path('agregar/<int:producto_id>/', views.agregar_producto, name='add'),
    path('agregar1/<int:producto_id>/', views.agregar_producto1, name='add1'),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name='del'),
    path('restar/<int:producto_id>/', views.restar_producto, name='sub'),
    path('limpiar/', views.limpiar_carrito, name='cls'),
]
