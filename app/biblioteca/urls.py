from django.urls import path

from . import views

urlpatterns = [
    path('libros/', views.lista_libros, name='lista_libros_biblioteca'),
    path('libros/crear/', views.crear_libro, name='crear_libro_biblioteca'),
    path('prestamos/', views.lista_prestamos, name='lista_prestamos_biblioteca'),
    path('prestamos/crear/', views.crear_prestamo, name='crear_prestamo_biblioteca'),
    path(
        'prestamos/<int:prestamo_id>/',
        views.detalle_prestamo,
        name='detalle_prestamo_biblioteca',
    ),
    path(
        'prestamos/<int:prestamo_id>/actualizar/',
        views.actualizar_estado_prestamo,
        name='actualizar_prestamo_biblioteca',
    ),
]

