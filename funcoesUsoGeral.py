from datetime import datetime
from django.contrib import messages

mensagensMaisUsadas = {
    'sucesso': 'Cadastro efetuado com sucesso !',
    'falha': 'Cadastro não efetuado !'
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
