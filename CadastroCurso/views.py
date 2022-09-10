from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(redirect_field_name='login-system')
def cadastraCurso(request):
    return render(request, 'cadastraCurso/cadastraCurso.html')


@login_required(redirect_field_name='login-system')
def cadastraGrade(request):
    return render(request, 'cadastraCurso/cadastraGrade.html')
