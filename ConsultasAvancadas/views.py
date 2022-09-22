from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FormConsulta


@login_required(redirect_field_name='login-system')
def consultas(request):
    if request.method != 'POST':
        formulario = FormConsulta(request.POST)
        return render(request, 'ConsultasAvancadas/consultaAvancada.html', {
            'form': formulario,
        })
    else:
        formulario = FormConsulta(request.POST)
        if formulario.is_valid():
            resposta = request.POST.get('pesquisa')
            return render(request, 'ConsultasAvancadas/consultaAvancada.html', {
                'form': formulario,
                'resp': resposta,
            })
        else:
            return render(request, 'ConsultasAvancadas/consultaAvancada.html', {
                'form': formulario,
                # 'resp': resposta,
            })
