from django.shortcuts import render, redirect
from cadastros import models
from django.contrib import messages
from django.db import connection
from django.contrib.auth.decorators import login_required
from funcoesUsoGeral import paginacao, mensagens, mensagensMaisUsadas, log


@log
def consultaGeral(modelo, nomeForeingKey: str, nomeColunaOrdenacao: str):
    return modelo.objects.prefetch_related(nomeForeingKey).order_by(nomeColunaOrdenacao)


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
    contexto = {
        'respPesquisa': '',
        'qtdTotalAlunos': '',
        'qtdPPaginaAluno': '',
        'consultaIdadeMedia': '',
        'consultaMenor18': '',
        'consultaEntre18E30': '',
        'consultaAcima30': '',
        'temporizador': '',
    }
    if request.method == 'GET':
        contexto['respPesquisa'], contexto['temporizador'] = consultaGeral(models.Aluno, 'endereco', 'nome_aluno')
        contexto['respPesquisa'] = paginacao(request, contexto['respPesquisa'], 20)
        contexto['qtdTotalAlunos'], contexto['qtdPPaginaAluno'] = models.Aluno.objects.count(), len(contexto['respPesquisa'])
        contexto['consultaIdadeMedia'], contexto['consultaMenor18'], contexto['consultaEntre18E30'], contexto['consultaAcima30'] = \
            consultaIdadeMedia(), consultaMenor18(), consultaEntre18E30(), consultaAcima30()
        contexto['temporizador'] = round(contexto['temporizador'], 4)
        messages.success(request, mensagensMaisUsadas['consSuc'])
        return render(request, 'ConsultasGerais/consultaAluno.html', contexto)


@login_required(redirect_field_name='login-system')
def consultaCurso(request):
    contexto = {
        'respPesquisa': '',
        'qtdCursos': '',
        'temporizador': '',
    }
    contexto['respPesquisa'], contexto['temporizador'] = consultaGeral(models.Curso, 'cod_dep', 'cod_dep')
    contexto['qtdCursos'] = len(contexto['respPesquisa'])
    contexto['temporizador'] = round(contexto['temporizador'], 4)
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
            contexto = {
                'respPesquisaAluno': '',
                'respPesquisaGrade': '',
                'qtdTotalPesquisa': '',
                'temporizador': '',
                'nomeAluno': '',
                'sobrenomeAluno': '',
            }
            cpf = request.GET.get('cpf')
            contexto['respPesquisaAluno'], contexto['temporizador'] = consultaDetalhesEscolaresAlunos(cpf)
            contexto['nomeAluno'], contexto['sobrenomeAluno'] = contexto['respPesquisaAluno'][0], contexto['respPesquisaAluno'][1]
            codCurso = contexto['respPesquisaAluno'][3]
            contexto['respPesquisaGrade'] = consultaMateriasCurso(codCurso)
            contexto['respPesquisaGrade'] = (materia[0] for materia in contexto['respPesquisaGrade'])
            contexto['qtdTotalPesquisa'], contexto['temporizador'] = len(contexto['respPesquisaAluno']), \
                round(contexto['temporizador'], 3)
            mensagens(request, 'suc', mensagensMaisUsadas['consSuc'])
            return render(request, 'ConsultasGerais/detalhesAlunos.html', contexto)
        except Exception:
            mensagens(request, 'err', f"{mensagensMaisUsadas['consFal']}... Aluno {cpf} não matriculado.")
            return redirect('cadastrar-matricula')


@login_required(redirect_field_name='login-system')
def detalhesCurso(request):
    if request.method != 'GET':
        return render(request, 'ConsultasGerais/detalhesCursos.html')
    else:
        try:
            contexto = {
                'respPesquisaCurso': '',
                'codCurso': '',
                'nomeCurso': '',
                'codGrade': '',
                'qtdDisciplinas': '',
                'qtdAlunos': '',
                'departamento': '',
                'temporizador': '',
            }
            codCurso = request.GET.get('codC')
            contexto['respPesquisaCurso'], contexto['temporizador'] = consultaDetalhesEscolaresCurso(codCurso)
            contexto['codCurso'], contexto['nomeCurso'], contexto['codGrade'] = \
                contexto['respPesquisaCurso'][0][0], contexto['respPesquisaCurso'][0][1], \
                contexto['respPesquisaCurso'][0][2]
            contexto['respPesquisaCurso'] = (tupla[3:] for tupla in contexto['respPesquisaCurso'])
            contexto['qtdAlunos'], contexto['qtdDisciplinas'], contexto['departamento'] = \
                consultaEstatisticaCurso(codCurso)
            contexto['temporizador'] = round(contexto['temporizador'], 3)
            mensagens(request, 'suc', mensagensMaisUsadas['consSuc'])
            return render(request, 'ConsultasGerais/detalhesCursos.html', contexto)
        except Exception as erro:
            mensagens(request, 'err', f'{mensagensMaisUsadas["consFal"]}... {erro}')
            return redirect('consulta-curso')
