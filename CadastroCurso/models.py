from cadastros.models import Curso, Grade
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django import forms


class FormCurso(ModelForm):
    class Meta:
        model = Curso
        fields = ['cod_c', 'nome_c', 'cod_dep']
        labels = {
            'cod_c': _('Código do Curso:'),
            'nome_c': _('Nome do Curso:'),
            'cod_dep': _('Código do Departamento:'),
        }

        widgets = {
            'nome_c': forms.TextInput(attrs={
                'placeholder': 'Digite o nome do curso.',
            }),
        }


class FormGrade(ModelForm):
    class Meta:
        model = Grade
        fields = ['cod_curso', 'cod_disciplina']
        labels = {
            'cod_curso': _('Código do Curso:'),
            'cod_disciplina': _('Código da Disciplina:'),
        }
