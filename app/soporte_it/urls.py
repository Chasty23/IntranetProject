from django.urls import path

from . import views

urlpatterns = [
    path('tickets/', views.lista_tickets, name='lista_tickets_soporte'),
    path('tickets/crear/', views.crear_ticket, name='crear_ticket_soporte'),
    path(
        'tickets/<int:ticket_id>/',
        views.detalle_ticket,
        name='detalle_ticket_soporte',
    ),
    path(
        'tickets/<int:ticket_id>/editar/',
        views.editar_ticket,
        name='editar_ticket_soporte',
    ),
    path(
        'tickets/<int:ticket_id>/gestionar/',
        views.gestionar_ticket,
        name='gestionar_ticket_soporte',
    ),
    path(
        'tickets/<int:ticket_id>/eliminar/',
        views.eliminar_ticket,
        name='eliminar_ticket_soporte',
    ),
]

