from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FormDisciplina, FormRequisito
from funcoesUsoGeral import dataServidor, verificadorNumerico, mensagens, mensagensMaisUsadas


@login_required(redirect_field_name='login-system')
def cadastroDisciplina(request):
    if request.method != 'POST':
        formularioDisc = FormDisciplina(request.POST)
        return render(request, 'cadastroDisciplina/cadastroDisciplina.html', {
            'formDisc': formularioDisc,
            'data': dataServidor(),
        })
    else:
        formularioDisc = FormDisciplina(request.POST)
        nomeDisc: str = request.POST.get('nome_disciplina')
        if verificadorNumerico(nomeDisc) and formularioDisc.is_valid():
            formularioDisc.save()
            mensagens(request, 'suc', mensagensMaisUsadas['sucesso'])
            return redirect('cadastra-disciplina')
        else:
            mensagens(request, 'err', f'O nome da Disciplina não pode conter números ... {mensagensMaisUsadas["falha"]}')
            formularioDisc = FormDisciplina(request.POST)
            return render(request, 'cadastroDisciplina/cadastroDisciplina.html', {
                'formDisc': formularioDisc,
                'data': dataServidor(),
            })


@login_required(redirect_field_name='login-system')
def cadastroRequisito(request):
    if request.method != 'POST':
        formularioReq = FormRequisito(request.POST)
        return render(request, 'cadastroDisciplina/cadastroRequisito.html', {
            'formReq': formularioReq,
            'data': dataServidor()
        })
    else:
        formularioReq = FormRequisito(request.POST)
        try:
            if formularioReq.is_valid():
                formularioReq.save()
                mensagens(request, 'suc', mensagensMaisUsadas['sucesso'])
                return redirect('cadastra-requisito')
            else:
                raise ValueError('Verifique sua entrada !')
        except ValueError as erro:
            mensagens(request, 'err', f'{mensagensMaisUsadas["falha"]}... {erro}')
            return render(request, 'cadastroDisciplina/cadastroRequisito.html', {
                'formReq': formularioReq,
                'data': dataServidor()
            })
