from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(redirect_field_name='login')
def cadastroProfessor(request):
    return render(request, 'cadastroProfessor/cadastroProfessor.html')


@login_required(redirect_field_name='login-system')
def cadastroContrato(request):
    return render(request, 'cadastroProfessor/cadastroContrato.html')
