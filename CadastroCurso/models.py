from cadastros.models import Curso
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _


class FormCurso(ModelForm):
    class Meta:
        model = Curso
        fields = ['cod_c', 'nome_c', 'cod_dep']
        # exclude = ()
        labels = {
            'cod_c': _('Código do Curso:'),
            'nome_c': _('Nome do Curso:'),
            'cod_dep': _('Código do Departamento:'),
        }
