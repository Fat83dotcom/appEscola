from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib import messages, auth
from datetime import datetime


def login(request):
    data = datetime.today()
    if request.method != 'POST':
        return render(request, 'Usuarios/login.html', {
            'data': data,
        })
    else:
        usuario = request.POST.get('nomeUsuario')
        senha = request.POST.get('senha')

        usuario = auth.authenticate(request, username=usuario, password=senha)

        if not usuario:
            messages.error(request, 'Usuario ou Senha incorreta !')
            return render(request, 'Usuarios/login.html', {
                'data': data,
            })
        else:
            auth.login(request, usuario)
            messages.success(request, 'Login efetuado com sucesso !')
            return redirect('index')


def logout(request):
    auth.logout(request)
    messages.warning(request, 'Você saiu, faça login para entrar novamente !')
    return redirect('login-system')
