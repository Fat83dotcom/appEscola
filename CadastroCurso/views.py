from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cadastros import models
from .models import FormCurso, FormGrade
from funcoesUsoGeral import dataServidor, verificadorNumerico, \
    mensagens, mensagensMaisUsadas
from django.core.paginator import Paginator


@login_required(redirect_field_name='login-system')
def cadastraCurso(request):
    dadosDepartamento = models.Departamento.objects.order_by('cod_dep')
    paginacao = Paginator(dadosDepartamento, 10)
    pagina = request.GET.get('p')
    dadosDepartamento = paginacao.get_page(pagina)
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
        try:
            if formularioCurso.is_valid():
                if not verificadorNumerico(campoNome):
                    mensagens(request, 'err', 'O nome do curso não pode conter números')
                    return render(request, 'cadastraCurso/cadastraCurso.html', {
                        'data': dataServidor(),
                        'formCurso': formularioCurso,
                        'dadosDep': dadosDepartamento,
                    })
                formularioCurso.save()
                mensagens(request, 'suc', mensagensMaisUsadas['sucesso'])
                return redirect('cadastra-curso')
            else:
                raise ValueError('Verifique sua entrada !')
        except ValueError as erro:
            mensagens(request, 'err', f"{mensagensMaisUsadas['falha']}... {erro}")
            return render(request, 'cadastraCurso/cadastraCurso.html', {
                'data': dataServidor(),
                'formCurso': formularioCurso,
                'dadosDep': dadosDepartamento,
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
        try:
            if formularioGrade.is_valid():
                formularioGrade.save()
                mensagens(request, 'suc', mensagensMaisUsadas['sucesso'])
                return redirect('cadastra-grade')
            else:
                raise ValueError('Verifique sua entrada !')
        except ValueError as erro:
            mensagens(request, 'err', f'{mensagensMaisUsadas["falha"]}... {erro}')
            return render(request, 'cadastraCurso/cadastraGrade.html', {
                'formGrade': formularioGrade,
                'data': dataServidor(),
            })
