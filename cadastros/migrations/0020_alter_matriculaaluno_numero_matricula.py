# Generated by Django 4.1.1 on 2022-09-25 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0019_matriculaaluno_numero_matricula_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matriculaaluno',
            name='numero_matricula',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]