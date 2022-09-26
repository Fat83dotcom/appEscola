from datetime import datetime
from django.contrib import messages
from time import time
from django.core.paginator import Paginator


mensagensMaisUsadas = {
    'sucesso': 'Cadastro efetuado com sucesso !',
    'falha': 'Cadastro não efetuado !',
    'consSuc': 'Consulta realizada com sucesso !',
    'consFal': 'Consulta não realizada',
}


def dataServidor() -> datetime:
    return datetime.today()


def verificadorNumerico(string: str) -> bool:
    '''Retorna False se houver um número na string'''
    for letra in string:
        if letra.isdigit():
            return False
    return True


def mensagens(request, tipo: str, mensagem: str):
    '''
        Parametro Tipo:
            'suc' -> Para mensagens de cadastros com sucesso.
            'war' -> Para mensagens de avisos.
            'err' -> Para mensagens de cadastros com erro.
    '''
    if tipo == 'suc':
        return messages.success(request, mensagem)
    elif tipo == 'war':
        return messages.warning(request, mensagem)
    else:
        return messages.error(request, mensagem)


def paginacao(request, query, nPaginas):
    return Paginator(query, nPaginas).get_page(request.GET.get('p'))


def log(funcao):
    def motor(*args) -> tuple:
        tIni = time()
        retornoFuncao = funcao(*args)
        tFim = time()
        return retornoFuncao, tFim - tIni
    return motor
