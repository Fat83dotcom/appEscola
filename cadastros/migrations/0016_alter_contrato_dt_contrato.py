# Generated by Django 4.1.1 on 2022-09-21 23:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0015_alter_grade_unique_together_grade_cod_grade_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='dt_contrato',
            field=models.DateField(default=datetime.datetime(2022, 9, 21, 20, 9, 33, 624022)),
        ),
    ]
