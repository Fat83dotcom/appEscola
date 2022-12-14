from cadastros.models import Aluno, Endereco, MatriculaAluno, AlunoDisciplina
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django import forms


class FormAluno(ModelForm):
    class Meta:
        model = Aluno
        fields = ['cpf', 'nome_aluno', 'sobrenome_aluno', 'dt_nasc', 'endereco']
        labels = {
            'cpf': _('CPF:'),
            'nome_aluno': _('Nome do Aluno:'),
            'sobrenome_aluno': _('Sobrenome do Aluno:'),
            'dt_nasc': _('Data Nascimento:'),
            'endereco': _('Endereço do Aluno:'),
        }

        widgets = {
            'cpf': forms.TextInput(attrs={
                'placeholder': 'Digite o CPF do Aluno.',
            }),
            'nome_aluno': forms.TextInput(attrs={
                'placeholder': 'Digite o nome do Aluno.',
            }),
            'sobrenome_aluno': forms.TextInput(attrs={
                'placeholder': 'Digite o Sobrenome do Aluno.',
            }),
            'dt_nasc': forms.DateInput(attrs={
                'placeholder': 'DD/MM/AAAA'
            }),
        }


class FormEndereco(ModelForm):
    class Meta:
        model = Endereco
        fields = ['logradouro', 'numero', 'bairro', 'complemento']
        labels = {
            'logradouro': _('Rua/Avenida:'),
            'numero': _('Número:'),
            'bairro': _('Bairro:'),
            'complemento': _('Complemento:'),
        }

        widgets = {
            'logradouro': forms.TextInput(attrs={
                'placeholder': 'Digite o logradouro do Aluno.',
            }),
            'numero': forms.TextInput(attrs={
                'placeholder': 'Digite o número da residência.'
            }),
            'bairro': forms.TextInput(attrs={
                'placeholder': 'Digite o bairro.'
            }),
            'complemento': forms.TextInput(attrs={
                'placeholder': 'Digite um complemento Ex.:(Apto, Referências, etc.).'
            }),
        }


class FormMatricula(ModelForm):
    class Meta:
        model = MatriculaAluno
        fields = ['cpf', 'cod_c']
        labels = {
            'cpf': _('CPF / Nome do Aluno:'),
            'cod_c': _('Código / Nome do Curso:'),
        }


class FormAlunoDisciplina(ModelForm):
    class Meta:
        model = AlunoDisciplina
        fields = ['cpf', 'cod_grade', 'qtd_creditos']
        labels = {
            'cpf': _('CPF / Nome do Aluno:'),
            'cod_grade': _('Código / Grade Curso:'),
            'qtd_creditos': _('Créditos:')
        }
