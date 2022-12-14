# Generated by Django 4.1.1 on 2022-09-21 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0014_aluno_dt_nasc'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='grade',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='grade',
            name='cod_grade',
            field=models.CharField(default='codGrade', max_length=10),
        ),
        migrations.AlterUniqueTogether(
            name='grade',
            unique_together={('cod_curso', 'cod_disciplina', 'cod_grade')},
        ),
    ]
