from django.contrib import admin
from .models import Libro, Prestamo

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'isbn', 'existencias')

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'libro', 'fecha_prestamo', 'devuelto')
