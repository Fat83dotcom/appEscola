from django import forms
# from django.forms import formset_factory


class FormConsulta(forms.Form):
    pesquisa = forms.CharField(label='Pesquisa', max_length=11, required=False)

    class Meta:
        widgets = {
            'pesquisa': forms.TextInput(attrs={
                'placeholder': 'Digite o CPF do aluno'
            })
        }

# formulario = formset_factory(FormConsulta)
