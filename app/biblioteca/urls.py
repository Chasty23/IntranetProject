from django.urls import path
from . import views

urlpatterns = [
    path('libros/', views.lista_libros, name='lista_libros'),
    path('libros/crear/', views.crear_libro, name='crear_libro'),
    path('prestamos/', views.lista_prestamos, name='lista_prestamos'),
    path('prestamos/crear/', views.crear_prestamo, name='crear_prestamo'),
    path('prestamos/<int:id>/', views.detalle_prestamo, name='detalle_prestamo'),
    path('prestamos/<int:id>/actualizar/', views.actualizar_prestamo, name='actualizar_prestamo'),
]
