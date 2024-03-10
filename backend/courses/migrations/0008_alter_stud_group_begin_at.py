# Generated by Django 5.0.1 on 2024-03-08 11:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_alter_stud_group_begin_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stud_group',
            name='begin_at',
            field=models.DateField(db_index=True, default=datetime.date(2024, 3, 8), verbose_name='Начало обучения'),
        ),
    ]
