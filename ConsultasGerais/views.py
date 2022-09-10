from django.shortcuts import render
from cadastros import models
from django.contrib import messages


def consultaAluno(request):
    # cruza a consulta da tabela Aluno com a chave estrangeira endereco!
    dadosAluno = models.Aluno.objects.prefetch_related('endereco')
    messages.success(request, 'Consulta realizada com sucesso !')

    return render(request, 'ConsultasGerais/consultaAluno.html', {
        'dadosJuntados': dadosAluno,
    })


def consultaCurso(request):
    return render(request, 'ConsultasGerais/consultaCurso.html')


def consultaProfessor(request):
    return render(request, 'ConsultasGerais/consultaProfessor.html')
