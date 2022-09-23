from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from funcoesUsoGeral import mensagens
from .models import FormConsulta
from cadastros.models import Aluno
from django.db.models import Q
# from datetime import datetime


def formatadorDatas(dados):
    try:
        d = datetime.strptime(dados, '%d/%m/%Y')
        return d.strftime('%Y-%m-%d')
    except Exception:
        return None


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
            try:
                pesquisa = request.POST.get('pesquisa')
                resultadoPesquisa = Aluno.objects.prefetch_related('endereco').order_by('nome_aluno').filter(
                    Q(cpf__icontains=pesquisa) | Q(nome_aluno__icontains=pesquisa) |
                    Q(sobrenome_aluno__icontains=pesquisa) | Q(dt_nasc=formatadorDatas(pesquisa))
                )
                print(resultadoPesquisa)
                print(len(resultadoPesquisa))
                if len(resultadoPesquisa) == 0:
                    mensagens(request, 'war', f'Não foram encotrados dados relacionados a {pesquisa}')
                    return render(request, 'ConsultasAvancadas/consultaAvancada.html', {
                        'form': formulario,
                    })
                return render(request, 'ConsultasAvancadas/consultaAvancada.html', {
                    'form': formulario,
                    'resp': resultadoPesquisa,
                })
            except Exception as erro:
                print(erro, 'aqui')
                return render(request, 'ConsultasAvancadas/consultaAvancada.html', {
                    'form': formulario,
                })
        else:
            return render(request, 'ConsultasAvancadas/consultaAvancada.html', {
                'form': formulario,
                # 'resp': resposta,
            })
