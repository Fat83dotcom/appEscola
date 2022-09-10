from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(redirect_field_name='login-system')
def cadastroDisciplina(request):
    return render(request, 'cadastroDisciplina/cadastroDisciplina.html')


@login_required(redirect_field_name='login-system')
def cadastroRequisito(request):
    return render(request, 'cadastroDisciplina/cadastroRequisito.html')
