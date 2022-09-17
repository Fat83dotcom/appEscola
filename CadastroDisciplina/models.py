from cadastros.models import Disciplina, Prerequisito
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django import forms


class FormDisciplina(ModelForm):
    class Meta():
        model = Disciplina
        fields = ['nome_disciplina', 'matricula_prof']
        labels = {
            'nome_disciplina': _('Nome Disciplina'),
            'matricula_prof': _('Matrícula Professor'),
        }
        widgets = {
            'nome_disciplina': forms.TextInput(attrs={
                'placeholder': 'Digite o Nome da Disciplina',
            }),
        }


class FormRequisito(ModelForm):
    class Meta:
        model = Prerequisito
        fields = ['cod_requisitante', 'cod_requisitado']
