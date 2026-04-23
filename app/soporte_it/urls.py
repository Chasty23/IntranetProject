from django.urls import path
from . import views

urlpatterns = [
    path('tickets/', views.lista_tickets, name='lista_tickets'),
    path('tickets/crear/', views.crear_ticket, name='crear_ticket'),
    path('tickets/<int:id>/', views.detalle_ticket, name='detalle_ticket'),
    path('tickets/<int:id>/editar/', views.editar_ticket, name='editar_ticket'),
    path('tickets/<int:id>/gestionar/', views.gestionar_ticket, name='gestionar_ticket'),
    path('tickets/<int:id>/eliminar/', views.eliminar_ticket, name='eliminar_ticket'),
]
