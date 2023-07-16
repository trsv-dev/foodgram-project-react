from colorfield.fields import ColorField
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from users.models import User


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


class Recipe(models.Model):
    """Модель для рецептов."""

    author = models.ForeignKey(
        User,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        help_text='Укажите автора рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='RecipeIngredient',
        blank=False,

    )
    tags = models.ManyToManyField(
        Tags,
        blank=False,

    )
    name = models.TextField(
        max_length=200,
        blank=False,
        null=False,
        verbose_name='Название',
        help_text='Укажите название рецепта'
    )
    text = models.TextField(
        max_length=200,
        blank=False,
        null=False,
        verbose_name='Описание',
        help_text='Введите описание рецепта'
    )
    cooking_time = models.IntegerField(
        blank=False,
        null=False,
        validators=(
            MinValueValidator(
                limit_value=1,
                message='Время приготовления не может быть меньше 1 минуты'
            ),
        ),
        verbose_name='Время приготовления',
        help_text='Укажите время приготовления в минутах'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время публикации'
    )

    # Добавить ingredients и image


class RecipeIngredient(models.Model):
    """Модель для связи рецептов и ингредиентов."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        help_text='Укажите рецепт'

    )
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        help_text='Выберите ингредиент'
    )
    amount = models.IntegerField(
        validators=(
            MinValueValidator(
                limit_value=1,
                message='Количество ингредиентов не может быть меньше 1'
            ),
        ),
        verbose_name='Количество',
        help_text='Укажите количество'
    )

    class Meta:
        verbose_name='Связь ингредиент/рецепт'
        verbose_name_plural = 'Связь ингредиенты/рецепты'

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'
