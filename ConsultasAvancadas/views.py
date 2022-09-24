from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from funcoesUsoGeral import mensagens
from .models import FormConsulta
from cadastros.models import Aluno
from django.db.models import Q
from django.core.paginator import Paginator


def formatadorDatas(dataEntrada):
    try:
        return datetime.strptime(dataEntrada, '%d/%m/%Y').strftime('%Y-%m-%d')
    except Exception:
        return None


def paginacao(request, query, nPaginas):
    return Paginator(query, nPaginas).get_page(request.GET.get('p'))


@login_required(redirect_field_name='login-system')
def consultas(request):
    formulario = FormConsulta(request.GET)
    if formulario.is_valid():
        try:
            pesquisa = request.GET.get('pesquisa')
            print(pesquisa)
            if pesquisa == '' or pesquisa is None:
                mensagens(request, 'war', 'Digite um nome, sobrenome, data de nascimento, cpf ou parte deles.')
                return render(request, 'ConsultasAvancadas/consultaAvancada.html', {
                    'form': formulario,
                })
            resultadoPesquisa = Aluno.objects.prefetch_related('endereco').order_by('nome_aluno').filter(
                Q(cpf__icontains=pesquisa) | Q(nome_aluno__icontains=pesquisa) |
                Q(sobrenome_aluno__icontains=pesquisa) | Q(dt_nasc=formatadorDatas(pesquisa))
            )
            if len(resultadoPesquisa) == 0:
                mensagens(request, 'war', f'Não foram encotrados dados relacionados a {pesquisa}')
                return render(request, 'ConsultasAvancadas/consultaAvancada.html', {
                    'form': formulario,
                })
            resultadoPesquisa = paginacao(request, resultadoPesquisa, 10)
            mensagens(request, 'suc', 'Pesquisa realizada com Sucesso')
            return render(request, 'ConsultasAvancadas/consultaAvancada.html', {
                'form': formulario,
                'resp': resultadoPesquisa,
            })
        except Exception as erro:
            mensagens(request, 'err', erro)
            return render(request, 'ConsultasAvancadas/consultaAvancada.html', {
                'form': formulario,
            })
    else:
        return render(request, 'ConsultasAvancadas/consultaAvancada.html', {
            'form': formulario,
        })
