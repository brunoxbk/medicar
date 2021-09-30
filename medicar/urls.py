"""medicar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
# from clinic import views
from django.conf import settings
from django.conf.urls.static import static
from clinic import views as view_clinic

urlpatterns = [
    path('admin/', admin.site.urls),
    path('especialidades/', view_clinic.EspecialidadeList.as_view(),
         name='lista-especialidade'),
    path('medicos/', view_clinic.MedicoList.as_view(), name='lista-medicos'),
    path('agendas/', view_clinic.AgendaList.as_view(), name='lista-agendas'),
    path('consultas/', view_clinic.ConsultaList.as_view(), name='lista-consultas'),
    path('consultas/<int:pk>/', view_clinic.ConsultaDetail.as_view(),
         name='apaga-consultas'),
    path('rest_auth/', include('rest_auth.urls')),
    path('rest_auth/registration/', include('rest_auth.registration.urls'))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
