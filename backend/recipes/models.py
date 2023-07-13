from colorfield.fields import ColorField
from django.core.validators import RegexValidator
from django.db import models


class Ingredients(models.Model):
    """Модель для ингредиентов."""

    name = models.CharField(
        max_length=150,
        db_index=True,
        verbose_name='Название ингредиента',
        help_text='Введите название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Единица измерения',
        help_text='Введите единицу измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}'


class Tags(models.Model):
    """Модель для тэгов."""

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название тэга',
        help_text='Введите название тэга'
    )
    color = ColorField(
        default='#00FF00',
        max_length=7,
        unique=True,
        verbose_name='Цвет',
        help_text='Цвет в HEX (Например, #00FF00)'
    )
    slug = models.CharField(
        max_length=200,
        validators=(
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='В слаге содержится недопустимый символ'
            ),
        ),
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return f'{self.slug}'
