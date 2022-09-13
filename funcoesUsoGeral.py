from datetime import datetime
from django.contrib import messages

mensagensMaisUsadas = {
    'sucesso': 'Cadastro efetuado com sucesso !',
    'falha': 'Cadastro não efetuado !'
}


def dataServidor() -> datetime:
    return datetime.today()


def verificadorNumerico(string: str) -> bool:
    for letra in string:
        if letra.isdigit():
            return False
    return True


def mensagens(request, tipo: str, mensagem: str):
    if tipo == 'success':
        return messages.success(request, mensagem)
    elif tipo == 'warnig':
        return messages.warning(request, mensagem)
    else:
        return messages.error(request, mensagem)
