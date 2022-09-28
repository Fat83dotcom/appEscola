from django.shortcuts import render
from cadastros import models
from django.contrib import messages
from django.db import connection
from django.contrib.auth.decorators import login_required
from funcoesUsoGeral import paginacao, mensagens, mensagensMaisUsadas


def idadeMedia() -> float:
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                'SELECT AVG(EXTRACT(YEAR FROM AGE(dt_nasc))) FROM cadastros_aluno')
            return float(round(cursor.fetchone()[0], 2))
        except Exception:
            return 0


def menor18() -> int:
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT COUNT(*) FROM cadastros_aluno WHERE EXTRACT(YEAR FROM AGE(dt_nasc))<18')
        return int(cursor.fetchone()[0])


def entre18E30() -> int:
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT COUNT(*) FROM cadastros_aluno WHERE EXTRACT(YEAR FROM AGE(dt_nasc)) BETWEEN 18 AND 30')
        return int(cursor.fetchone()[0])


def acima30() -> int:
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT COUNT(*) FROM cadastros_aluno WHERE EXTRACT(YEAR FROM AGE(dt_nasc))>30')
        return int(cursor.fetchone()[0])


def dadosAlunos(cpf):
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT nome_aluno, sobrenome_aluno,dt_nasc, cadastros_curso.cod_c, nome_c,"
            f"numero_matricula, dt_matricula FROM cadastros_aluno, cadastros_matriculaaluno,"
            f"cadastros_curso WHERE cadastros_aluno.cpf='{cpf}' AND "
            "cadastros_aluno.cpf=cadastros_matriculaaluno.cpf AND "
            "cadastros_matriculaaluno.cod_c=cadastros_curso.cod_c")
        return cursor.fetchone()


@login_required(redirect_field_name='login-system')
def consultaAluno(request):
    if request.method == 'GET':
        # cruza a consulta da tabela Aluno com a chave estrangeira endereco!
        dadosAluno = models.Aluno.objects.prefetch_related(
            'endereco').order_by('nome_aluno')
        dadosAluno = paginacao(request, dadosAluno, 20)
        estatAlunosQtdT = models.Aluno.objects.count()
        estatAlunosQtdP = len(dadosAluno)
        messages.success(request, mensagensMaisUsadas['consSuc'])
        return render(request, 'ConsultasGerais/consultaAluno.html', {
            'dadosJuntados': dadosAluno,
            'estatAlunoT': estatAlunosQtdT,
            'estatAlunoP': estatAlunosQtdP,
            'idadeMedia': idadeMedia(),
            'menor18': menor18(),
            'entre18e30': entre18E30(),
            'acima30': acima30(),
        })


@login_required(redirect_field_name='login-system')
def consultaCurso(request):
    resultadoPesquisa = models.Curso.objects.prefetch_related('cod_dep')
    nAlunosCursos = models.MatriculaAluno.objects.select_related('cod_c')
    print(nAlunosCursos)
    nCursos = len(resultadoPesquisa)
    contexto = {
        'result': resultadoPesquisa,
        'nCursos': nCursos
    }
    mensagens(request, 'suc', mensagensMaisUsadas['consSuc'])
    return render(request, 'ConsultasGerais/consultaCurso.html', contexto)


@login_required(redirect_field_name='login-system')
def consultaProfessor(request):
    return render(request, 'ConsultasGerais/consultaProfessor.html')


@login_required(redirect_field_name='login-system')
def detalhesAluno(request):
    if request.method != 'GET':
        return render(request, 'ConsultasGerais/detalhesAlunos.html')
    else:
        cpf = request.GET.get('cpf')
        dadoAluno = dadosAlunos(cpf)
        print(dadoAluno)
        return render(request, 'ConsultasGerais/detalhesAlunos.html', {
            'dados': dadoAluno
        })
