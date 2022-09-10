from django.urls import path
from . import views

urlpatterns = [
    path('cadastraraluno/', views.cadastroAluno, name='cadastrar-aluno'),
    path('cadastrarendereco/', views.cadastroEndereco, name='cadastrar-endereco'),
    path('cadastrarmatricula/', views.cadastroMatricula, name='cadastrar-matricula'),
    path('cadastrar-alunoDisciplina/', views.cadastroDisciplina, name='cadastrar-alunoDisciplina'),
]
