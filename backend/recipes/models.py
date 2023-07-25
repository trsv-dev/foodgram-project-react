from colorfield.fields import ColorField
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from users.models import User


class Ingredients(models.Model):
    """Модель для ингредиентов."""

    name = models.CharField(
        max_length=150,
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
        related_name='recipes',
        help_text='Укажите автора рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tags,
        blank=False,
        related_name='recipes',
        verbose_name='Тэг',
        help_text='Выберите подходящие тэги'

    )
    image = models.ImageField(
        default=None,
        null=True,
        upload_to='recipes/images/',
        verbose_name='Изображение',
        help_text='Загрузите изображение'
    )
    name = models.TextField(
        max_length=200,
        blank=False,
        null=False,
        verbose_name='Название',
        help_text='Укажите название рецепта'
    )
    text = models.TextField(
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
        verbose_name='Время приготовления (мин.)',
        help_text='Укажите время приготовления в минутах'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время публикации'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.name}'


class RecipeIngredient(models.Model):
    """Модель для связи рецептов и ингредиентов."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes_ingredients',
        verbose_name='Рецепт',
        help_text='Укажите рецепт'

    )
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='recipes_ingredients',
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
        verbose_name = 'Связь ингредиент/рецепт'
        verbose_name_plural = 'Связь ингредиенты/рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique_ingredient_recipe',
            ),
        )
        ordering = ('id',)

    def __str__(self):
        return (
            f'Ингредиенты для "{self.recipe}": {self.ingredient} - '
            f'{self.amount}'
        )


class Favorites(models.Model):
    """Модель для избранного (избранные рецепты)."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
        help_text='Выберите пользователя'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
        help_text='Выберите рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_recipe_favorites'
            ),
        )
        ordering = ('id',)

    def __str__(self):
        return f'{self.user} добавил в избранное "{self.recipe}"'


class ShoppingList(models.Model):
    """Класс для списка покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Пользователь',
        help_text='Выберите пользователя'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Рецепт',
        help_text='Выберите рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_recipe_shopping_list'
            ),
        )

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в список покупок'
