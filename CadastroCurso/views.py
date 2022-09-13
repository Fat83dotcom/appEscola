from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cadastros import models
from .models import FormCurso, FormGrade
from funcoesUsoGeral import dataServidor, verificadorNumerico, \
    mensagens, mensagensMaisUsadas


@login_required(redirect_field_name='login-system')
def cadastraCurso(request):
    dadosDepartamento = models.Departamento.objects.order_by('cod_dep')
    if request.method != 'POST':
        formularioCurso = FormCurso(request.POST)
        return render(request, 'cadastraCurso/cadastraCurso.html', {
            'data': dataServidor(),
            'formCurso': formularioCurso,
            'dadosDep': dadosDepartamento,
        })
    else:
        formularioCurso = FormCurso(request.POST)
        campoNome: str = request.POST.get('nome_c')
        if formularioCurso.is_valid():
            if not verificadorNumerico(campoNome):
                mensagens(request, 'error', 'O nome do curso não pode conter números')
                return redirect('cadastra-curso')

            formularioCurso.save()
            mensagens(request, 'success', mensagensMaisUsadas['sucesso'])
            return redirect('cadastra-curso')

        else:
            mensagens(request, 'error', mensagensMaisUsadas['falha'])
            return render(request, 'cadastraCurso/cadastraCurso.html', {
                'data': dataServidor(),
                'formCurso': formularioCurso
            })


@login_required(redirect_field_name='login-system')
def cadastraGrade(request):
    if request.method != 'POST':
        formularioGrade = FormGrade(request.POST)
        return render(request, 'cadastraCurso/cadastraGrade.html', {
            'formGrade': formularioGrade,
            'data': dataServidor(),
        })
    else:
        formularioGrade = FormGrade(request.POST)
        if formularioGrade.is_valid():
            formularioGrade.save()
            mensagens(request, 'success', mensagensMaisUsadas['sucesso'])
            return redirect('cadastra-grade')
        else:
            mensagens(request, 'error', mensagensMaisUsadas['falha'])
            return redirect('cadastra-grade')
