from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FormContrato, FormProfessor
from funcoesUsoGeral import dataServidor, verificadorNumerico, mensagens, mensagensMaisUsadas


@login_required(redirect_field_name='login')
def cadastroProfessor(request):
    if request.method != 'POST':
        formularioProf = FormProfessor(request.POST)
        return render(request, 'cadastroProfessor/cadastroProfessor.html', {
            'formProf': formularioProf,
            'data': dataServidor(),
        })
    else:
        formularioProf = FormProfessor(request.POST)
        nomeProf = request.POST.get('nome_prof')
        sNomeProf = request.POST.get('sobrenome_prof')
        try:
            if verificadorNumerico(nomeProf) and verificadorNumerico(sNomeProf) and \
                    formularioProf.is_valid():
                formularioProf.save()
                mensagens(request, 'suc', mensagensMaisUsadas['sucesso'])
                return redirect('cadastrar-professor')
            else:
                if verificadorNumerico(nomeProf) is False or verificadorNumerico(sNomeProf) is False:
                    mensagens(request, 'war', 'O nome ou sobrenome não pode conter números "')
                raise ValueError('Verifique sua entrada !')
        except ValueError as erro:
            mensagens(request, 'err', f'{mensagensMaisUsadas["falha"]}... {erro}')
            return render(request, 'cadastroProfessor/cadastroProfessor.html', {
                'formProf': formularioProf,
                'data': dataServidor(),
            })


@login_required(redirect_field_name='login-system')
def cadastroContrato(request):
    if request.method != 'POST':
        formularioContrato = FormContrato(request.POST)
        return render(request, 'cadastroProfessor/cadastroContrato.html', {
            'formContr': formularioContrato
        })
    else:
        formularioContrato = FormContrato(request.POST)
        try:
            if formularioContrato.is_valid():
                formularioContrato.save()
                mensagens(request, 'suc', mensagensMaisUsadas['sucesso'])
                return redirect('cadastrar-contrato')
            else:
                raise ValueError
        except ValueError as erro:
            mensagens(request, 'err', f'{mensagensMaisUsadas["falha"]} ... {erro}')
            return render(request, 'cadastroProfessor/cadastroContrato.html', {
                'formContr': formularioContrato
            })
