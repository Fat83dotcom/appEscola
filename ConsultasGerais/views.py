from django.shortcuts import render
from cadastros import models
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import connection


def idadeMedia() -> float:
    cursor = connection.cursor()
    cursor.execute('SELECT AVG(EXTRACT(YEAR FROM AGE(dt_nasc))) FROM cadastros_aluno')
    return float(round(cursor.fetchone()[0], 2))


def menor18() -> int:
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM cadastros_aluno WHERE EXTRACT(YEAR FROM AGE(dt_nasc))<18')
    return int(cursor.fetchone()[0])


def entre18E30() -> int:
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM cadastros_aluno WHERE EXTRACT(YEAR FROM AGE(dt_nasc)) BETWEEN 18 AND 30')
    return int(cursor.fetchone()[0])


def acima30() -> int:
    cursor = connection.create_cursor()
    cursor.execute('SELECT COUNT(*) FROM cadastros_aluno WHERE EXTRACT(YEAR FROM AGE(dt_nasc))>30')
    return int(cursor.fetchone()[0])


def consultaAluno(request):
    if request.method == 'GET':
        # cruza a consulta da tabela Aluno com a chave estrangeira endereco!
        dadosAluno = models.Aluno.objects.prefetch_related(
            'endereco').order_by('nome_aluno')
        paginator = Paginator(dadosAluno, 20)
        pagina = request.GET.get('p')
        dadosAluno = paginator.get_page(pagina)
        estatAlunosQtdT = models.Aluno.objects.count()
        estatAlunosQtdP = len(dadosAluno)
        messages.success(request, 'Consulta realizada com sucesso !')
        return render(request, 'ConsultasGerais/consultaAluno.html', {
            'dadosJuntados': dadosAluno,
            'estatAlunoT': estatAlunosQtdT,
            'estatAlunoP': estatAlunosQtdP,
            'idadeMedia': idadeMedia(),
            'menor18': menor18(),
            'entre18e30': entre18E30(),
            'acima30': acima30(),
        })


def consultaCurso(request):
    return render(request, 'ConsultasGerais/consultaCurso.html')


def consultaProfessor(request):
    return render(request, 'ConsultasGerais/consultaProfessor.html')
