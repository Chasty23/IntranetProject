from django.contrib import admin

from .models import Libro, Prestamo


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        'autor',
        'isbn',
        'ejemplares_totales',
        'ejemplares_disponibles',
        'activo',
    )
    list_filter = ('activo',)
    search_fields = ('titulo', 'autor', 'isbn')


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = (
        'libro',
        'expediente',
        'fecha_prestamo',
        'fecha_devolucion',
        'estado',
    )
    list_filter = ('estado',)
    search_fields = (
        'libro__titulo',
        'expediente__carnet',
        'expediente__usuario__username',
    )

