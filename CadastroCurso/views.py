from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from cadastros import models
from .models import FormCurso
from django.contrib import messages


def verificadorNumerico(string: str) -> bool:
    for letra in string:
        if letra.isdigit():
            return False
    return True


@login_required(redirect_field_name='login-system')
def cadastraCurso(request):
    data = datetime.today()
    dadosDepartamento = models.Departamento.objects.order_by('cod_dep')
    if request.method != 'POST':
        formularioCurso = FormCurso(request.POST)
        return render(request, 'cadastraCurso/cadastraCurso.html', {
            'data': data,
            'formCurso': formularioCurso,
            'dadosDep': dadosDepartamento,
        })
    else:
        formularioCurso = FormCurso(request.POST)

        campoNome: str = request.POST.get('nome_c')

        if formularioCurso.is_valid():
            if not verificadorNumerico(campoNome):
                messages.error(request, 'O nome do curso não pode conter números')
                return redirect('cadastra-curso')

            formularioCurso.save()
            messages.success(request, 'Cadastro efetuado com sucesso !')
            return redirect('cadastra-curso')

        else:
            messages.error(request, 'Cadastro não efetuado !')
            return render(request, 'cadastraCurso/cadastraCurso.html', {
                'data': data,
                'formCurso': formularioCurso
            })


@login_required(redirect_field_name='login-system')
def cadastraGrade(request):
    return render(request, 'cadastraCurso/cadastraGrade.html')
