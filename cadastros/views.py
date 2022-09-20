from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.decorators import login_required


@login_required(redirect_field_name='login-system')
def index(request):
    data = datetime.today()
    return render(request, 'contatos/index.html', {
        'data': data
    })


def info(request):
    return render(request, 'contatos/info.html')