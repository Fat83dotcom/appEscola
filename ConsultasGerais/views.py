from django.shortcuts import render, redirect
from cadastros import models
from django.contrib import messages
from django.db import connection
from django.contrib.auth.decorators import login_required
from funcoesUsoGeral import paginacao, mensagens, mensagensMaisUsadas, log


def consultaIdadeMedia() -> float:
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                'SELECT AVG(EXTRACT(YEAR FROM AGE(dt_nasc))) FROM cadastros_aluno')
            return float(round(cursor.fetchone()[0], 2))
        except Exception:
            return 0


def consultaMenor18() -> int:
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT COUNT(*) FROM cadastros_aluno WHERE EXTRACT(YEAR FROM AGE(dt_nasc))<18')
        return int(cursor.fetchone()[0])


def consultaEntre18E30() -> int:
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT COUNT(*) FROM cadastros_aluno WHERE EXTRACT(YEAR FROM AGE(dt_nasc)) BETWEEN 18 AND 30'
        )
        return int(cursor.fetchone()[0])


def consultaAcima30() -> int:
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT COUNT(*) FROM cadastros_aluno WHERE EXTRACT(YEAR FROM AGE(dt_nasc))>30')
        return int(cursor.fetchone()[0])


@log
def consultaGeralAlunos(modelo):
    return modelo.objects.prefetch_related(
            'endereco').order_by('nome_aluno')


@log
def consultaDetalhesEscolaresAlunos(cpf) -> tuple | None:
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT nome_aluno, sobrenome_aluno, dt_nasc, cadastros_curso.cod_c, nome_c, '
            'numero_matricula, dt_matricula FROM cadastros_aluno INNER JOIN cadastros_matriculaaluno '
            'ON(cadastros_aluno.cpf=cadastros_matriculaaluno.cpf) INNER JOIN cadastros_curso '
            'ON(cadastros_matriculaaluno.cod_c=cadastros_curso.cod_c)WHERE cadastros_aluno.cpf=%s '
            'GROUP BY nome_aluno, sobrenome_aluno, dt_nasc, cadastros_curso.cod_c, nome_c, '
            'numero_matricula, dt_matricula ORDER BY nome_aluno', (cpf,)
        )
        return cursor.fetchone()


@log
def consultaDetalhesEscolaresCurso(codCurso) -> list[tuple]:
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT cadastros_curso.cod_c, nome_c, cod_grade, cod_d, nome_disciplina, cadastros_professor.matricula_prof, '
            'nome_prof, sobrenome_prof FROM cadastros_curso INNER JOIN cadastros_matriculaaluno '
            'ON(cadastros_curso.cod_c=cadastros_matriculaaluno.cod_c) INNER JOIN cadastros_grade '
            'ON(cadastros_matriculaaluno.cod_c=cadastros_grade.cod_curso) INNER JOIN cadastros_disciplina '
            'ON(cadastros_grade.cod_disciplina=cadastros_disciplina.cod_d) INNER JOIN cadastros_professor '
            'ON(cadastros_disciplina.matricula_prof=cadastros_professor.matricula_prof) WHERE cadastros_matriculaaluno.cod_c=%s'
            'GROUP BY cadastros_curso.cod_c, nome_c, cod_grade, cod_d, nome_disciplina, cadastros_professor.matricula_prof, '
            'sobrenome_prof, nome_prof ORDER BY nome_prof', (codCurso,)
        )
        return cursor.fetchall()


def consultaMateriasCurso(codCurso) -> list[tuple]:
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT nome_disciplina FROM cadastros_grade, cadastros_disciplina,"
            "cadastros_curso WHERE cadastros_grade.cod_curso=%s AND cadastros_grade.cod_disciplina=cadastros_disciplina.cod_d AND "
            "cadastros_grade.cod_curso=cadastros_curso.cod_c order by nome_disciplina", (codCurso,)
        )
        return cursor.fetchall()


def consultaEstatisticaCurso(codCurso) -> tuple | None:
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT COUNT(cpf) FROM cadastros_matriculaaluno WHERE cod_c=%s', (codCurso, )
        )
        nAlunos = cursor.fetchone()[0]
        cursor.execute(
            'SELECT COUNT(cod_disciplina) FROM cadastros_grade WHERE cod_curso=%s', (codCurso, )
        )
        nDisciplinas = cursor.fetchone()[0]
        cursor.execute(
            'SELECT nome_dep FROM cadastros_curso INNER JOIN cadastros_departamento '
            'ON(cadastros_curso.cod_dep=cadastros_departamento.cod_dep) WHERE cod_c=%s', (codCurso, )
        )
        departamento = cursor.fetchone()[0]
        return (nAlunos, nDisciplinas, departamento)


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
            'idadeMedia': consultaIdadeMedia(),
            'menor18': consultaMenor18(),
            'entre18e30': consultaEntre18E30(),
            'acima30': consultaAcima30(),
            'temp': round(log, 3),
            'nResult': estatAlunosQtdT
        })


@login_required(redirect_field_name='login-system')
def consultaCurso(request):
    resultadoPesquisa = models.Curso.objects.prefetch_related('cod_dep')
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
            dadoAluno, log = consultaDetalhesEscolaresAlunos(cpf)
            codCurso = dadoAluno[3]
            grade = consultaMateriasCurso(codCurso)
            grade = (materia[0] for materia in grade)
            mensagens(request, 'suc', mensagensMaisUsadas['consSuc'])
            return render(request, 'ConsultasGerais/detalhesAlunos.html', {
                'dadosA': dadoAluno,
                'dadosG': grade,
                'temp': round(log, 3),
                'eResult': len(dadoAluno),
            })
        except Exception:
            mensagens(request, 'err', f"{mensagensMaisUsadas['consFal']}... Aluno {cpf} não matriculado.")
            return redirect('cadastrar-matricula')


@login_required(redirect_field_name='login-system')
def detalhesCurso(request):
    if request.method != 'GET':
        return render(request, 'ConsultasGerais/detalhesCursos.html')
    else:
        try:
            codCurso = request.GET.get('codC')
            resultadoPesquisa, log = consultaDetalhesEscolaresCurso(codCurso)
            codDisciplina, nomeDisciplina, codGrade = resultadoPesquisa[0][0],\
                resultadoPesquisa[0][1], resultadoPesquisa[0][2]
            nEstat = len(resultadoPesquisa)
            resultadoPesquisa = (tupla[3::] for tupla in resultadoPesquisa)
            nAlunos, nDisciplinas, departamento = consultaEstatisticaCurso(codCurso)
            mensagens(request, 'suc', mensagensMaisUsadas['consSuc'])
            return render(request, 'ConsultasGerais/detalhesCursos.html', {
                'dadosC': resultadoPesquisa,
                'codC': codDisciplina,
                'nomeC': nomeDisciplina,
                'codG': codGrade,
                'temp': round(log, 3),
                'eResult': nEstat,
                'estatAluno': nAlunos,
                'estatDisci': nDisciplinas,
                'estatDep': departamento,
            })
        except Exception as erro:
            mensagens(request, 'err', f'{mensagensMaisUsadas["consFal"]}... {erro}')
            return redirect('consulta-curso')
