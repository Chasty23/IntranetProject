from django.urls import path
from . import views

urlpatterns = [
    path('personal/', views.lista_empleados, name='lista_empleados'),
    path('personal/detalle/<int:empleado_id>/', views.detalle_empleado, name='detalle_empleado'),
]