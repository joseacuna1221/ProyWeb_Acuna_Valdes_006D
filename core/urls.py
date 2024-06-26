from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name="Home"),
    path('productos/', views.productos, name="productos"),
    path('Acercade/', views.Acercade, name="Acercade"),
    path('Mascotas/', views.Mascotas, name="Mascotas"),
    path('registrar/', views.registrar, name="registrar"),
    path('carrito/', views.carrito, name="carrito"),
    path('logout/', views.cerrar, name="cerrar"),
    path('crear_producto/', views.crear_producto, name='crear_producto'),
    path('modificar/<int:id>/', views.modificar_producto, name='modificar_producto'),
    path('eliminar_producto_admin/<int:id>/', views.eliminar_producto_admin, name='eliminar_producto_admin'),
    path('tienda/', views.tienda, name='tienda'),
    path('agregar/<int:id>/', views.agregar_producto, name='agregar_producto'),
    path('limpiar-carrito/', views.limpiar_carrito, name='limpiar_carrito'),
    path('generar-boleta/', views.generar_boleta, name='generar_boleta'),
    path('productos/mascotas/', views.lista_mascotas_salvadas, name='lista_mascotas_salvadas'),
    path('lista_productos/', views.lista_productos, name='lista_productos'),
    path('restar/<int:id>/', views.restar_producto_carrito, name='restar_producto_carrito'),
    path('agregar/<int:id>/', views.agregar_producto_carrito, name='agregar_producto_carrito'),
    path('eliminar/<int:id>/', views.eliminar_producto_carrito, name='eliminar_producto_carrito'),
    path('generar_boleta/', views.generar_boleta, name='generar_boleta'),

]

