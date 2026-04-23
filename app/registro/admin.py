from django.contrib import admin
from .models import CicloAcademico, Inscripcion

@admin.register(CicloAcademico)
class CicloAcademicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'activo')

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'materia', 'ciclo', 'fecha_inscripcion')
