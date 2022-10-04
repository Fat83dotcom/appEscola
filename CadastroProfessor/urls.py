from django.urls import path
from . import views

urlpatterns = [
    path('cadastrarprofessor/', views.cadastroProfessor, name='cadastrar-professor'),
]
