# Generated by Django 4.1 on 2022-09-04 22:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='endereco',
            field=models.ForeignKey(db_column='endereco', on_delete=django.db.models.deletion.DO_NOTHING, to='cadastros.endereco'),
        ),
    ]
