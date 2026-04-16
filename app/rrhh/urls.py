from django.urls import path
from . import views

urlpatterns = [
    path('personal/', views.lista_empleados, name='lista_empleados'),
]