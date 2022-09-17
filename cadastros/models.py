from django.db import models


class Aluno(models.Model):
    cpf = models.CharField(primary_key=True, max_length=11)
    nome_aluno = models.CharField(max_length=100)
    sobrenome_aluno = models.CharField(max_length=100)
    endereco = models.ForeignKey(
        'Endereco', on_delete=models.DO_NOTHING, db_column='endereco')

    def __str__(self) -> str:
        return f'{self.cpf}: {self.nome_aluno.title()} {self.sobrenome_aluno.title()}'


class Endereco(models.Model):
    cod_end = models.AutoField(primary_key=True)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=255)
    complemento = models.CharField(
        max_length=255, blank=True, null=True, default='ND')

    def __str__(self) -> str:
        return f'{self.logradouro.title()}, {self.numero}, {self.bairro.title()}'

    class Meta:
        unique_together = ['logradouro', 'numero', 'bairro']


class Grade(models.Model):
    id_grade = models.AutoField(primary_key=True)
    cod_curso = models.ForeignKey(
        'Curso', models.DO_NOTHING, db_column='cod_curso', null=False)
    cod_disciplina = models.ForeignKey(
        'Disciplina', models.DO_NOTHING, db_column='cod_disciplina', null=False)

    def __str__(self) -> str:
        return f'Cod / Disciplina: {self.cod_disciplina} | Cod / Curso: {self.cod_curso}'

    class Meta:
        unique_together = ['cod_curso', 'cod_disciplina']


class AlunoDisciplina(models.Model):
    cod_aluno_disciplina = models.AutoField(primary_key=True)
    cpf = models.ForeignKey(
        Aluno, models.DO_NOTHING, db_column='cpf', null=False)
    cod_grade = models.ForeignKey(
        Grade, models.DO_NOTHING, db_column='id_grade', null=False)
    qtd_creditos = models.IntegerField()

    class Meta:
        unique_together = ['cpf', 'cod_grade']


class Contrato(models.Model):
    matricula_prof = models.OneToOneField(
        'Professor', models.DO_NOTHING, db_column='matricula_prof', primary_key=True)
    dt_contrato = models.DateField()
    cod_dep = models.ForeignKey(
        'Departamento', models.DO_NOTHING, db_column='cod_dep', blank=True, null=True)

    def __str__(self) -> str:
        return str(self.matricula_prof)


class Curso(models.Model):
    cod_c = models.AutoField(primary_key=True)
    nome_c = models.CharField(unique=True, max_length=255)
    cod_dep = models.ForeignKey(
        'Departamento', models.DO_NOTHING, db_column='cod_dep')

    def __str__(self) -> str:
        return f'{self.cod_c} / {self.nome_c}'


class Departamento(models.Model):
    cod_dep = models.AutoField(primary_key=True)
    nome_dep = models.CharField(unique=True, max_length=255)

    def __str__(self) -> str:
        return self.nome_dep


class Disciplina(models.Model):
    cod_d = models.AutoField(primary_key=True)
    nome_disciplina = models.CharField(unique=True, max_length=255)
    matricula_prof = models.ForeignKey(
        'Professor', models.DO_NOTHING, db_column='matricula_prof')

    def __str__(self) -> str:
        return f'{self.cod_d} / {self.nome_disciplina}'


class MatriculaAluno(models.Model):
    cpf = models.ForeignKey(
        Aluno, models.DO_NOTHING, db_column='cpf', primary_key=True)
    cod_c = models.ForeignKey(Curso, models.DO_NOTHING, db_column='cod_c')
    dt_matricula = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return str(self.cpf)


class Prerequisito(models.Model):
    cod_requisicao = models.AutoField(primary_key=True)
    cod_requisitante = models.ForeignKey(Disciplina, models.DO_NOTHING, db_column='cod_requisitante',
                                         related_name='cod_requisitado')
    cod_requisitado = models.ForeignKey(
        Disciplina, models.DO_NOTHING, db_column='cod_requisitado')

    def __str__(self) -> str:
        return self.cod_requisitante

    class Meta:
        unique_together = ['cod_requisitante', 'cod_requisitado']


class Professor(models.Model):
    matricula_prof = models.AutoField(primary_key=True)
    nome_prof = models.CharField(max_length=255)
    sobrenome_prof = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'{self.matricula_prof} / {self.nome_prof}'

    class Meta:
        unique_together = ['matricula_prof', 'nome_prof', 'sobrenome_prof']
