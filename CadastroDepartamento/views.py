from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from funcoesUsoGeral import mensagens, mensagensMaisUsadas, dataServidor, verificadorNumerico
from .models import FormDepartamento


@login_required(redirect_field_name='login-system')
def cadastrarDepartamento(request):
    if request.method != 'POST':
        formularioDep = FormDepartamento(request.POST)
        return render(request, 'cadastroDepartamento/cadastroDepartamento.html', {
            'formDep': formularioDep,
            'data': dataServidor()
        })
    else:
        formularioDep = FormDepartamento(request.POST)
        nomeDep: str = request.POST.get('nome_dep')
        if verificadorNumerico(nomeDep) and formularioDep.is_valid():
            formularioDep.save()
            mensagens(request, 'suc', mensagensMaisUsadas['sucesso'])
            return redirect('cadastrar-departamento')
        else:
            formularioDep = FormDepartamento(request.POST)
            mensagens(request, 'err', f"O nome não pode conter números... {mensagensMaisUsadas['falha']}")
            return render(request, 'cadastroDepartamento/cadastroDepartamento.html', {
                'formDep': formularioDep,
                'data': dataServidor()
            })
