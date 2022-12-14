# Generated by Django 4.1.1 on 2022-09-13 22:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies: list = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('cod_dep', models.AutoField(primary_key=True, serialize=False)),
                ('nome_dep', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('cod_end', models.AutoField(primary_key=True, serialize=False)),
                ('logradouro', models.CharField(max_length=30)),
                ('numero', models.CharField(max_length=10)),
                ('bairro', models.CharField(max_length=20)),
                ('complemento', models.CharField(blank=True,
                 default='ND', max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('matricula_prof', models.AutoField(
                    primary_key=True, serialize=False)),
                ('nome_prof', models.CharField(max_length=30)),
                ('sobrenome_prof', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Teste',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('testi', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('cod_d', models.AutoField(primary_key=True, serialize=False)),
                ('nome_disciplina', models.CharField(max_length=90, unique=True)),
                ('matricula_prof', models.ForeignKey(db_column='matricula_prof',
                 on_delete=django.db.models.deletion.DO_NOTHING, to='cadastros.professor')),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('cod_c', models.AutoField(primary_key=True, serialize=False)),
                ('nome_c', models.CharField(max_length=50, unique=True)),
                ('cod_dep', models.ForeignKey(db_column='cod_dep',
                 on_delete=django.db.models.deletion.DO_NOTHING, to='cadastros.departamento')),
            ],
        ),
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('cpf', models.CharField(max_length=11,
                 primary_key=True, serialize=False)),
                ('nome_aluno', models.CharField(max_length=30)),
                ('sobrenome_aluno', models.CharField(max_length=20)),
                ('endereco', models.ForeignKey(db_column='endereco',
                 on_delete=django.db.models.deletion.DO_NOTHING, to='cadastros.endereco')),
            ],
        ),
        migrations.CreateModel(
            name='Prerequisito',
            fields=[
                ('cod_requisitante', models.OneToOneField(db_column='cod_requisitante', on_delete=django.db.models.deletion.DO_NOTHING,
                 primary_key=True, related_name='cod_requisitado', serialize=False, to='cadastros.disciplina')),
                ('cod_requisitado', models.ForeignKey(db_column='cod_requisitado',
                 on_delete=django.db.models.deletion.DO_NOTHING, to='cadastros.disciplina')),
            ],
        ),
        migrations.CreateModel(
            name='MatriculaAluno',
            fields=[
                ('cpf', models.ForeignKey(db_column='cpf', on_delete=django.db.models.deletion.DO_NOTHING,
                 primary_key=True, serialize=False, to='cadastros.aluno')),
                ('dt_matricula', models.DateField(auto_now=True)),
                ('cod_c', models.ForeignKey(db_column='cod_c',
                 on_delete=django.db.models.deletion.DO_NOTHING, to='cadastros.curso')),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id_grade', models.AutoField(primary_key=True, serialize=False)),
                ('cod_curso', models.ForeignKey(db_column='cod_curso',
                 on_delete=django.db.models.deletion.DO_NOTHING, to='cadastros.curso')),
                ('cod_disciplina', models.ForeignKey(db_column='cod_disciplina',
                 on_delete=django.db.models.deletion.DO_NOTHING, to='cadastros.disciplina')),
            ],
            options={
                'unique_together': {('cod_curso', 'cod_disciplina')},
            },
        ),
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('matricula_prof', models.OneToOneField(db_column='matricula_prof',
                 on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='cadastros.professor')),
                ('dt_contrato', models.DateField()),
                ('cod_dep', models.ForeignKey(blank=True, db_column='cod_dep', null=True,
                 on_delete=django.db.models.deletion.DO_NOTHING, to='cadastros.departamento')),
            ],
        ),
        migrations.CreateModel(
            name='AlunoDisciplina',
            fields=[
                ('cpf', models.OneToOneField(db_column='cpf', on_delete=django.db.models.deletion.DO_NOTHING,
                 primary_key=True, serialize=False, to='cadastros.aluno')),
                ('qtd_creditos', models.IntegerField()),
                ('cod_d', models.ForeignKey(db_column='cod_d',
                 on_delete=django.db.models.deletion.DO_NOTHING, to='cadastros.disciplina')),
            ],
        ),
    ]
