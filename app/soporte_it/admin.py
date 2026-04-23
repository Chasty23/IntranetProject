from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'solicitante', 'prioridad', 'estado', 'tecnico_asignado', 'fecha_creacion')
