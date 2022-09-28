from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from funcoesUsoGeral import mensagens
from .models import FormConsulta
from cadastros.models import Aluno
from django.db.models import Q, Value
from django.db.models.functions import Concat
from funcoesUsoGeral import paginacao, log


def formatadorDatas(dataEntrada):
    try:
        return datetime.strptime(dataEntrada, '%d/%m/%Y').strftime('%Y-%m-%d')
    except Exception:
        return None


@log
def pesquisaAvancada(pesquisa):
    nomeCompleto = Concat('nome_aluno', Value(' '), 'sobrenome_aluno')
    return Aluno.objects.prefetch_related('endereco').order_by(
                'nome_aluno').annotate(nomeCompleto=nomeCompleto).filter(
                Q(cpf__icontains=pesquisa) |
                Q(nome_aluno__icontains=pesquisa) |
                Q(sobrenome_aluno__icontains=pesquisa) |
                Q(dt_nasc=formatadorDatas(pesquisa)) |
                Q(nomeCompleto__icontains=pesquisa))


@login_required(redirect_field_name='login-system')
def consultas(request):
    formulario = FormConsulta(request.GET)
    contexto = {
        'form': '',
        'resp': '',
        'nResult': '',
        'nResultPag': '',
        'temp': ''
    }
    if formulario.is_valid():
        try:
            pesquisa = request.GET.get('pesquisa')
            if pesquisa == '' or pesquisa is None or pesquisa == ' ':
                mensagens(request, 'war', 'Digite um nome, sobrenome, data de nascimento, cpf ou parte deles.')
                return render(request, 'ConsultasAvancadas/consultaAvancada.html', {
                    'form': formulario,
                    'nResult': 0,
                })
            resultadoPesquisa, log = pesquisaAvancada(pesquisa)
            contexto['nResult'] = len(resultadoPesquisa)
            if len(resultadoPesquisa) == 0:
                mensagens(request, 'war', f'Não foram encotrados dados relacionados a {pesquisa}')
                return render(request, 'ConsultasAvancadas/consultaAvancada.html', {
                    'form': formulario,
                    'nResult': 0,
                })
            resultadoPesquisa = paginacao(request, resultadoPesquisa, 10)
            contexto['nResultPag'] = len(resultadoPesquisa)
            contexto['form'] = formulario
            contexto['resp'] = resultadoPesquisa
            contexto['temp'] = round(log, 3)
            mensagens(request, 'suc', 'Pesquisa realizada com Sucesso')
            return render(request, 'ConsultasAvancadas/consultaAvancada.html', contexto)
        except Exception as erro:
            mensagens(request, 'err', erro)
            return render(request, 'ConsultasAvancadas/consultaAvancada.html', {
                'form': formulario,
                'nResult': 0,
            })
    else:
        return render(request, 'ConsultasAvancadas/consultaAvancada.html', {
            'form': formulario,
            'nResult': 0,
        })
