from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FormDisciplina
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
    return render(request, 'cadastroDisciplina/cadastroRequisito.html')
