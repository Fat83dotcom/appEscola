from django.shortcuts import render
from cadastros import models
from django.contrib import messages
from django.core.paginator import Paginator


def consultaAluno(request):
    if request.method == 'GET':
        # cruza a consulta da tabela Aluno com a chave estrangeira endereco!
        dadosAluno = models.Aluno.objects.prefetch_related('endereco')
        paginacao = Paginator(dadosAluno, 20)
        pagina = request.GET.get('p')
        dadosAluno = paginacao.get_page(pagina)

        estatAlunosQtdT = models.Aluno.objects.count()
        estatAlunosQtdP = len(dadosAluno)
        messages.success(request, 'Consulta realizada com sucesso !')
        return render(request, 'ConsultasGerais/consultaAluno.html', {
            'dadosJuntados': dadosAluno,
            'estatAlunoT': estatAlunosQtdT,
            'estatAlunoP': estatAlunosQtdP
        })


def consultaCurso(request):
    return render(request, 'ConsultasGerais/consultaCurso.html')


def consultaProfessor(request):
    return render(request, 'ConsultasGerais/consultaProfessor.html')
