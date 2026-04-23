from django.urls import path

from . import views

urlpatterns = [
    path('inscripciones/', views.lista_inscripciones, name='lista_inscripciones_registro'),
    path('inscripciones/crear/', views.crear_inscripcion, name='crear_inscripcion_registro'),
    path(
        'inscripciones/<int:inscripcion_id>/',
        views.detalle_inscripcion,
        name='detalle_inscripcion_registro',
    ),
    path(
        'inscripciones/<int:inscripcion_id>/eliminar/',
        views.eliminar_inscripcion,
        name='eliminar_inscripcion_registro',
    ),
    path('ciclos/', views.lista_ciclos, name='lista_ciclos_registro'),
    path('ciclos/crear/', views.crear_ciclo, name='crear_ciclo_registro'),
]

