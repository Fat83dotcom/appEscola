from django.contrib import admin
from .models import Aluno, Curso, Disciplina, Departamento, Professor
from .models import Endereco, MatriculaAluno, Grade, Prerequisito


class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('matricula_prof', 'nome_prof')


class AlunoAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'nome_aluno', 'sobrenome_aluno')


class MatAlunoAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'cod_c', 'dt_matricula')


class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('cod_d', 'nome_disciplina')


class CursoAdmin(admin.ModelAdmin):
    list_display = ('cod_c', 'nome_c')


class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('cod_dep', 'nome_dep')


class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('cod_end', 'logradouro', 'numero', 'bairro')


# class GradeAdmin(admin.ModelAdmin):
#     list_display = ('id_grade', 'nome_c', 'nome_disciplina')


admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Disciplina, DisciplinaAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Endereco, EnderecoAdmin)
admin.site.register(MatriculaAluno, MatAlunoAdmin)
admin.site.register(Grade)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Prerequisito)
