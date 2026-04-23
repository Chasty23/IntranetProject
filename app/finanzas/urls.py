from django.urls import path
from . import views

urlpatterns = [
    path('estado-cuenta/', views.estado_cuenta, name='estado_cuenta'),
]