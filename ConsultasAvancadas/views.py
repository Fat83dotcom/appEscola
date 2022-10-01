from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from funcoesUsoGeral import mensagens
from .models import FormConsulta
from cadastros.models import Aluno
from django.db.models import Q, Value
from django.db.models.functions import Concat
from funcoesUsoGeral import paginacao, log, mensagensMaisUsadas


def formatadorDatas(dataEntrada):
    try:
        return datetime.strptime(dataEntrada, '%d/%m/%Y').strftime('%Y-%m-%d')
    except Exception:
        return None


@log
def pesquisaAvancada(pesquisa, modelo):
    nomeCompleto = Concat('nome_aluno', Value(' '), 'sobrenome_aluno')
    return modelo.objects.prefetch_related('endereco').order_by(
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
        'respPesquisa': '',
        'resultadoTotalEstatistica': '',
        'resultadoPPagina': '',
        'temporizador': '',
    }
    if formulario.is_valid():
        try:
            pesquisa = request.GET.get('pesquisa')
            if pesquisa == '' or pesquisa is None or pesquisa == ' ':
                mensagens(request, 'war', 'Digite um nome, sobrenome, data de nascimento, cpf ou parte deles.')
                return render(request, 'ConsultasAvancadas/consultaAvancada.html', {
                    'form': formulario,
                    'resultadoTotalEstatistica': 0,
                })
            contexto['respPesquisa'], contexto['temporizador'] = pesquisaAvancada(pesquisa, Aluno)
            contexto['resultadoTotalEstatistica'] = len(contexto['respPesquisa'])
            if len(contexto['respPesquisa']) == 0:
                mensagens(request, 'war', f'Não foram encotrados dados relacionados a {pesquisa}')
                return render(request, 'ConsultasAvancadas/consultaAvancada.html', {
                    'form': formulario,
                    'resultadoTotalEstatistica': 0,
                })
            contexto['respPesquisa'] = paginacao(request, contexto['respPesquisa'], 10)
            contexto['resultadoPPagina'] = len(contexto['respPesquisa'])
            contexto['form'] = formulario
            contexto['temporizador'] = round(contexto['temporizador'], 3)
            mensagens(request, 'suc', mensagensMaisUsadas['consSuc'])
            return render(request, 'ConsultasAvancadas/consultaAvancada.html', contexto)
        except Exception as erro:
            mensagens(request, 'err', erro)
            return render(request, 'ConsultasAvancadas/consultaAvancada.html', {
                'form': formulario,
                'resultadoTotalEstatistica': 0,
            })
    else:
        return render(request, 'ConsultasAvancadas/consultaAvancada.html', {
            'form': formulario,
            'resultadoTotalEstatistica': 0,
        })
