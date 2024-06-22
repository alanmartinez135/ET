from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name = 'inicio'),
    path('correa/', views.correa, name = 'correa'),
    path('bandana/', views.bandana, name = 'bandana'),
    path('identificador/', views.identificador, name = 'identificador'),
]
