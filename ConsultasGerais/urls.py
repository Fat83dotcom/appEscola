from django.urls import path
from . import views


urlpatterns = [
    path('aluno/', views.consultaAluno, name='consulta-aluno'),
    path('curso/', views.consultaCurso, name='consulta-curso'),
    path('professor/', views.consultaProfessor, name='consulta-professor'),
    path('detalhes-aluno/', views.detalhesAluno, name='detalhes-aluno'),
    path('detalhes-curso/', views.detalhesCurso, name='detalhes-curso'),
    path('detalhes-professor/', views.detalhesProfessor, name='detalhes-professor'),
]
