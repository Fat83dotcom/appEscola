from cadastros.models import Professor, Contrato
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django import forms


class FormProfessor(ModelForm):
    class Meta:
        model = Professor
        fields = ['nome_prof', 'sobrenome_prof']
        labels = {
            'nome_prof': _('Nome Professor:'),
            'sobrenome_prof': _('Sobrenome Professor:')
        }
        widgets = {
            'nome_prof': forms.TextInput(attrs={
                'placeholder': 'Digite o nome do Professor',
            }),
            'sobrenome_prof': forms.TextInput(attrs={
                'placeholder': 'Digite o sobrenome do professor'
            })
        }


class FormContrato(ModelForm):
    class Meta:
        model = Contrato
        fields = ['matricula_prof', 'cod_dep', 'dt_contrato']
        labels = {
            'matricula_prof': _('Matrícula Professor:'),
            'dt_contrato': _('Data Contrato:'),
            'cod_dep': _('Código Departamento',)
        }
        widgets = {
            'dt_contrato': forms.DateInput(attrs={
                'placeholder': 'DD/MM/AAAA',
            }),
        }
