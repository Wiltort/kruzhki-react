# Generated by Django 3.2.6 on 2022-03-26 11:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Groups', '0003_auto_20220325_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientsinGroup',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_list', to='Groups.ingredient', verbose_name='Рецепты'),
        ),
        migrations.AlterField(
            model_name='ingredientsinGroup',
            name='Group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_in_Group', to='Groups.Group', verbose_name='Ингредиенты'),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_favourites', to='Groups.Group', verbose_name='Избранные у пользователей')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='Избранные рецепты')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
            },
        ),
    ]
