from django.shortcuts import render, redirect
from django.contrib import messages
from cadastros import models
from .models import FormAluno, FormEndereco, FormMatricula, FormAlunoDisciplina
from django.contrib.auth.decorators import login_required
from funcoesUsoGeral import dataServidor
from django.core.paginator import Paginator


@login_required(redirect_field_name='login-system')
def cadastroAluno(request):
    if request.method != 'POST':
        dadosEndereco = models.Endereco.objects.order_by('-cod_end')
        paginacao = Paginator(dadosEndereco, 20)
        pagina = request.GET.get('p')
        dadosEndereco = paginacao.get_page(pagina)

        formularioAluno = FormAluno(request.POST)
        return render(request, 'cadastroAluno/cadastroAluno.html', {
            'formulario': formularioAluno,
            'dadosEnd': dadosEndereco,
            'data': dataServidor(),
        })

    formularioAluno = FormAluno(request.POST)

    if not formularioAluno.is_valid():
        formularioAluno = FormAluno(request.POST)
        messages.error(request, 'Cadastro não efetuado !')
        return render(request, 'cadastroAluno/cadastroAluno.html', {
            'formulario': formularioAluno,
            'dadosEnd': dadosEndereco,
            'data': dataServidor(),
        })
    else:
        cpf = request.POST.get('cpf')
        try:
            if int(cpf):
                if len(cpf) == 11:
                    formularioAluno.save()
                    messages.success(request, 'Cadastro efetuado com sucesso !')
                    return redirect('cadastrar-aluno')
                else:
                    formularioAluno = FormAluno(request.POST)
                    messages.error(request, 'O CPF deve conter 11 números !')
                    return render(request, 'cadastroAluno/cadastroAluno.html', {
                        'formulario': formularioAluno,
                        'dadosEnd': dadosEndereco,
                        'data': dataServidor(),
                        })
        except Exception:
            formularioAluno = FormAluno(request.POST)
            messages.error(request, 'O CPF deve conter somente números !')
            return render(request, 'cadastroAluno/cadastroAluno.html', {
                'formulario': formularioAluno,
                'dadosEnd': dadosEndereco,
                'data': dataServidor(),
                })


@login_required(redirect_field_name='login-system')
def cadastroEndereco(request):
    if request.method != 'POST':
        formularioEndereco = FormEndereco()
        return render(request, 'cadastroAluno/cadastroEndereco.html', {
            'formularioEndereco': formularioEndereco,
            'data': dataServidor(),
        })

    formularioEndereco = FormEndereco(request.POST)

    if not formularioEndereco.is_valid():
        formularioEndereco = FormEndereco(request.POST)
        messages.error(request, 'Verifique as entradas !')
        return render(request, 'cadastroAluno/cadastroEndereco.html', {
            'formularioEndereco': formularioEndereco,
            'data': dataServidor(),
        })
    else:
        formularioEndereco.save()
        messages.success(request, 'Cadastro efetuado com sucesso!')
        return redirect('cadastrar-endereco')


@login_required(redirect_field_name='login-system')
def cadastroMatricula(request):
    if request.method != 'POST':
        formularioMatricula = FormMatricula(request.POST)
        return render(request, 'cadastroAluno/cadastroMatricula.html', {
            'formMatricula': formularioMatricula,
            'data': dataServidor(),
        })

    formularioMatricula = FormMatricula(request.POST)

    if not formularioMatricula.is_valid():
        formularioMatricula = FormMatricula(request.POST)
        messages.error(request, 'Matricula inválida !')
        return render(request, 'cadastroAluno/cadastroMatricula.html', {
            'formMatricula': formularioMatricula,
            'data': dataServidor(),
        })
    else:
        formularioMatricula.save()
        messages.success(request, 'Matricula efetuado com Sucesso !')
        return redirect('cadastrar-matricula')


@login_required(redirect_field_name='login-system')
def cadastroDisciplina(request):
    if request.method != 'POST':
        formularioDisciplina = FormAlunoDisciplina(request.POST)
        return render(request, 'cadastroAluno/cadastroDisciplina.html', {
            'formDisciplina': formularioDisciplina,
            'data': dataServidor(),
        })

    formularioDisciplina = FormAlunoDisciplina(request.POST)

    if not formularioDisciplina.is_valid():
        formularioDisciplina = FormAlunoDisciplina(request.POST)
        messages.error(request, 'Por favor, confira os dados !')
        return render(request, 'cadastroAluno/cadastroDisciplina.html', {
            'formDisciplina': formularioDisciplina,
            'data': dataServidor(),
        })
    else:
        qtdCreditos = request.POST.get('qtd_creditos')

        if int(qtdCreditos) < 0:
            formularioDisciplina = FormAlunoDisciplina(request.POST)
            messages.warning(request, 'Quantidade de créditos não pode ser um número negativo !')
            return render(request, 'cadastroAluno/cadastroDisciplina.html', {
                'formDisciplina': formularioDisciplina,
                'data': dataServidor(),
            })

        formularioDisciplina.save()
        messages.success(request, 'Cadastro efetuado com Sucesso !')
        return redirect('cadastrar-alunoDisciplina')
