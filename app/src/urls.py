
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth import views as auth_views # Import this!

urlpatterns = [
    path('admin/', admin.site.urls),
    path('academico/', include('academico.urls')),
    path('', TemplateView.as_view(template_name='index.html')),
    path('rrhh/', include('rrhh.urls')),
    path('finanzas/', include('finanzas.urls')),
    path('soporte-it/', include('soporte_it.urls')),
    path('registro/', include('registro.urls')),
    path('biblioteca/', include('biblioteca.urls')),
    path('', TemplateView.as_view(template_name='index.html')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
