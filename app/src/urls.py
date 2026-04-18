
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('academico/', include('academico.urls')),
    path('rrhh/', include('rrhh.urls')),
    path('finanzas/', include('finanzas.urls')),
    # ESTA URL ES DE PRUEBA , SIMULA EL HOME /
    path('', RedirectView.as_view(url='/academico/notas/')),
]
