# Generated by Django 4.1.1 on 2022-09-14 22:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0003_alunodisciplina_cod_grade_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alunodisciplina',
            name='cod_grade',
            field=models.ForeignKey(db_column='id_grade', on_delete=django.db.models.deletion.DO_NOTHING, to='cadastros.grade'),
        ),
        migrations.AlterField(
            model_name='alunodisciplina',
            name='cpf',
            field=models.ForeignKey(db_column='cpf', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='cadastros.aluno'),
        ),
    ]
