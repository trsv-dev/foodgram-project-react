# Generated by Django 3.2.3 on 2023-07-29 17:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_recipeingredient_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='amount',
            field=models.IntegerField(help_text='Укажите количество', validators=[django.core.validators.MinValueValidator(limit_value=1, message='Количество ингредиентов не может быть меньше 1')], verbose_name='Количество'),
        ),
    ]
