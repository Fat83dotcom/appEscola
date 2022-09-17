from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FormProfessor
from funcoesUsoGeral import dataServidor


@login_required(redirect_field_name='login')
def cadastroProfessor(request):
    if request.method != 'POST':
        formularioProf = FormProfessor(request.POST)
        return render(request, 'cadastroProfessor/cadastroProfessor.html', {
            'formProf': formularioProf,
            'data': dataServidor(),
        })
    else:
        formularioProf = FormProfessor()


@login_required(redirect_field_name='login-system')
def cadastroContrato(request):
    return render(request, 'cadastroProfessor/cadastroContrato.html')
