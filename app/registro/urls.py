from django.urls import path
from . import views

urlpatterns = [
    path('inscripciones/', views.lista_inscripciones, name='lista_inscripciones'),
    path('inscripciones/crear/', views.crear_inscripcion, name='crear_inscripcion'),
    path('inscripciones/<int:id>/', views.detalle_inscripcion, name='detalle_inscripcion'),
    path('inscripciones/<int:id>/eliminar/', views.eliminar_inscripcion, name='eliminar_inscripcion'),
    path('ciclos/', views.lista_ciclos, name='lista_ciclos'),
    path('ciclos/crear/', views.crear_ciclo, name='crear_ciclo'),
]
