# Generated by Django 5.0.1 on 2024-02-18 08:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='attending',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='attending', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='stud_group',
            name='students',
            field=models.ManyToManyField(limit_choices_to={'is_staff': False}, related_name='stud_groups', to=settings.AUTH_USER_MODEL, verbose_name='Студенты'),
        ),
        migrations.DeleteModel(
            name='Student',
        ),
    ]
