
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('academico/', include('academico.urls')),
    path('', TemplateView.as_view(template_name='index.html')),
]
