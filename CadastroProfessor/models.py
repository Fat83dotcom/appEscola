from cadastros.models import Professor
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django import forms


class FormProfessor(ModelForm):
    class Meta:
        model = Professor
        fields = ['nome_prof', 'sobrenome_prof',  ]
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
