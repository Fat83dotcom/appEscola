from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import FormCurso


@login_required(redirect_field_name='login-system')
def cadastraCurso(request):
    data = datetime.today()
    if request.method != 'POST':
        formularioCurso = FormCurso(request.POST)
        return render(request, 'cadastraCurso/cadastraCurso.html', {
            'data': data,
            'formCurso': formularioCurso
        })


@login_required(redirect_field_name='login-system')
def cadastraGrade(request):
    return render(request, 'cadastraCurso/cadastraGrade.html')
