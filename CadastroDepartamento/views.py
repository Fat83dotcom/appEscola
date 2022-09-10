from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(redirect_field_name='login-system')
def cadastrarDepartamento(request):
    return render(request, 'cadastroDepartamento/cadastroDepartamento.html')
