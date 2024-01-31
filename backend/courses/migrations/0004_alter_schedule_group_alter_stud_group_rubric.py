# Generated by Django 4.2.7 on 2023-11-24 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_rubric_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='schedule', to='courses.stud_group'),
        ),
        migrations.AlterField(
            model_name='stud_group',
            name='rubric',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='stud_groups', to='courses.rubric'),
        ),
    ]
