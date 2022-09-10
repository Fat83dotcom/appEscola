from django.urls import path
from . import views

urlpatterns = [
    path('cadastardepartamento/', views.cadastrarDepartamento, name='cadastrar-departamento'),
]
