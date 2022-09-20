"""cadastro_simples URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cadastros.urls')),
    path('cadastro-a/', include('CadastroAlunos.urls')),
    path('cadastro-c/', include('CadastroCurso.urls')),
    path('cadastro-dep/', include('CadastroDepartamento.urls')),
    path('cadastro-disc/', include('CadastroDisciplina.urls')),
    path('cadastro-p/', include('CadastroProfessor.urls')),
    path('consulta-s/', include('ConsultasGerais.urls')),
    path('consulta-a/', include('ConsultasAvancadas.urls')),
    path('accounts/', include('Usuarios.urls')),
]
