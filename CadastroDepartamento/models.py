from cadastros.models import Departamento
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django import forms


class FormDepartamento(ModelForm):
    class Meta:
        model = Departamento
        fields = ['nome_dep']
        labels = {
            'nome_dep': _('Nome Departamento:')
        }
        widgets = {
            'nome_dep': forms.TextInput(attrs={
                'placeholder': 'Digite o Nome do Departamento',
            }),
        }
