from django.shortcuts import render, redirect
from cadastros import models
from django.contrib import messages
from django.db import connection
from django.contrib.auth.decorators import login_required
from funcoesUsoGeral import paginacao, mensagens, mensagensMaisUsadas, log


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
            'SELECT COUNT(*) FROM cadastros_aluno WHERE EXTRACT(YEAR FROM AGE(dt_nasc)) BETWEEN 18 AND 30'
        )
        return int(cursor.fetchone()[0])


def acima30() -> int:
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT COUNT(*) FROM cadastros_aluno WHERE EXTRACT(YEAR FROM AGE(dt_nasc))>30')
        return int(cursor.fetchone()[0])


@log
def consultaGeralAlunos(modelo):
    return modelo.objects.prefetch_related(
            'endereco').order_by('nome_aluno')


@log
def detalhesEscolaresAlunos(cpf) -> tuple | None:
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT nome_aluno, sobrenome_aluno, dt_nasc, cadastros_curso.cod_c, nome_c, "
            "numero_matricula, dt_matricula FROM cadastros_aluno, cadastros_matriculaaluno, "
            "cadastros_curso WHERE cadastros_aluno.cpf=%s AND "
            "cadastros_aluno.cpf=cadastros_matriculaaluno.cpf AND "
            "cadastros_matriculaaluno.cod_c=cadastros_curso.cod_c", (cpf,)
        )
        return cursor.fetchone()


def materiasCurso(codCurso) -> list[tuple]:
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT nome_disciplina FROM cadastros_grade, cadastros_disciplina,"
            "cadastros_curso WHERE cadastros_grade.cod_curso=%s AND cadastros_grade.cod_disciplina=cadastros_disciplina.cod_d AND "
            "cadastros_grade.cod_curso=cadastros_curso.cod_c order by nome_disciplina", (codCurso,)
        )
        return cursor.fetchall()


@login_required(redirect_field_name='login-system')
def consultaAluno(request):
    if request.method == 'GET':
        # cruza a consulta da tabela Aluno com a chave estrangeira endereco!
        dadosAluno, log = consultaGeralAlunos(models.Aluno)
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
            'temp': round(log, 3),
            'nResult': estatAlunosQtdT
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
        try:
            cpf = request.GET.get('cpf')
            dadoAluno, log = detalhesEscolaresAlunos(cpf)
            codCurso = dadoAluno[3]
            grade = materiasCurso(codCurso)
            grade = (materia[0] for materia in grade)
            mensagens(request, 'suc', mensagensMaisUsadas['consSuc'])
            return render(request, 'ConsultasGerais/detalhesAlunos.html', {
                'dadosA': dadoAluno,
                'dadosG': grade,
                'temp': round(log, 3),
                'nResult': len(dadoAluno)
            })
        except Exception:
            mensagens(request, 'err', f"{mensagensMaisUsadas['consFal']}... Aluno {cpf} não matriculado.")
            return redirect('cadastrar-matricula')
