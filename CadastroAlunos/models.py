from cadastros.models import Aluno, Endereco, MatriculaAluno, AlunoDisciplina
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _


class FormAluno(ModelForm):
    class Meta:
        model = Aluno
        fields = ['cpf', 'nome_aluno', 'sobrenome_aluno', 'endereco']
        # exclude = ()
        labels = {
            'cpf': _('CPF:'),
            'nome_aluno': _('Nome do Aluno:'),
            'sobrenome_aluno': _('Sobrenome do Aluno:'),
            'endereco': _('Endereço do Aluno:')
        }

        def clean(self):
            return self.cleaned_data['nome_aluno'].title()


class FormEndereco(ModelForm):
    class Meta:
        model = Endereco
        exclude = ()


class FormMatricula(ModelForm):
    class Meta:
        model = MatriculaAluno
        exclude = ()


class FormAlunoDisciplina(ModelForm):
    class Meta:
        model = AlunoDisciplina
        exclude = ()
