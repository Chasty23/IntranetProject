from django.contrib import admin

from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        'estado',
        'solicitante',
        'tecnico_asignado',
        'fecha_creacion',
    )
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('titulo', 'descripcion', 'solicitante__username')

