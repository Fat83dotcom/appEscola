from django.shortcuts import render


def consultas(request):
    return render(request, 'ConsultasAvancadas/consultaAvancada.html')
