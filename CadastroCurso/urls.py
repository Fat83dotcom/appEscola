from django.urls import path
from . import views

urlpatterns = [
    path('cadastracurso/', views.cadastraCurso, name='cadastra-curso'),
    path('cadastragrade/', views.cadastraGrade, name='cadastra-grade'),
]
