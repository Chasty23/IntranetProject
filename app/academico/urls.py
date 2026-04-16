from django.urls import path
from . import views

urlpatterns = [
    # Ruta para ver las notas (Nivel Consulta/Modificación)
    path('notas/', views.lista_notas, name='lista_notas'),
    
    # Ruta para editar notas (Nivel Modificación)
    path('notas/editar/<int:nota_id>/', views.editar_nota, name='editar_nota'),
]