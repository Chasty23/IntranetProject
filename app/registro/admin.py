from django.contrib import admin

from .models import CicloAcademico, Inscripcion


@admin.register(CicloAcademico)
class CicloAcademicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre',)


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('expediente', 'materia', 'ciclo', 'fecha_registro')
    list_filter = ('ciclo',)
    search_fields = (
        'expediente__carnet',
        'expediente__usuario__username',
        'materia__nombre',
    )

