# Generated by Django 3.2.6 on 2022-04-08 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Groups', '0011_ingredientsinGroup_unique_ingredient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='Group',
            name='image',
            field=models.ImageField(upload_to='backend_media/Groups/', verbose_name='Изображение'),
        ),
    ]