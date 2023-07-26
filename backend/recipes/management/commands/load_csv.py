from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from recipes.management.commands._load_cvs_func import load_func


class Command(BaseCommand):
    """Наполнение БД тестовыми данными из файлов .csv."""

    help = 'Загрузка тестовых файлов .csv в базу данных'

    def handle(self, *args, **options):
        try:
            load_func(self)

        except IntegrityError:
            raise CommandError(
                'База данных нуждается в очистке перед импортом. '
                'Удалите базу данных и выполните "python manage.py migrate"'
            )

        except FileNotFoundError:
            raise CommandError(
                'Файлы формата .csv в /data не найдены')

        except Exception:
            raise CommandError(
                'Неожиданная ошибка работы импорта load_csv,'
            )

        self.stdout.write(self.style.SUCCESS(
            'Все данные из csv-файлов загружены в базу данных'
            )
        )
