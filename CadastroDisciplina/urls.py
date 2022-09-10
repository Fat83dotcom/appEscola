from django.urls import path
from . import views

urlpatterns = [
    path('cadastrardisciplina/', views.cadastroDisciplina, name='cadastra-disciplina'),
    path('cadastrarequisito/', views.cadastroRequisito, name='cadastra-requisito')
]
