# Generated by Django 4.1.1 on 2022-09-17 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0009_alter_prerequisito_cod_requisicao'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='prerequisito',
            unique_together={('cod_requisitante', 'cod_requisitado')},
        ),
    ]
