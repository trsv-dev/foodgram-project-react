from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя."""

    ADMIN = 'admin'
    USER = 'user'
    ROLE_CHOICES = [
        (ADMIN, 'Администратор'),
        (USER, 'Пользователь'),
    ]

    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Эл. почта',
        help_text='Введите электронную почту'
    )
    username = models.CharField(
        validators=(
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='В имени пользователя разрешены '
                        'только символы . @ + - _ и пробел'
            ),
        ),
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Пользователь',
        help_text='Имя пользователя'
    )
    first_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name='Имя',
        help_text='Введите имя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name='Фамилия',
        help_text='Введите фамилию',
    )
    role = models.CharField(
        choices=ROLE_CHOICES,
        default=USER,
        max_length=150,
        blank=True,
        verbose_name='Роль',
        help_text='Выберите роль'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN
