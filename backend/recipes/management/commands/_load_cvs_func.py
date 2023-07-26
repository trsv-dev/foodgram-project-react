import csv
import sys
import time

from foodgram.settings import BASE_DIR
from recipes.management.commands.load_functions import (load_ingredients,
                                                        load_users, load_tags)
from recipes.models import Ingredients, Tags
from users.models import User

# Если потребуется добавить импорты, то можно
# добавить сюда название модели и файл для импорта.
CSV_DATA = {
    Ingredients: 'ingredients.csv',
    User: 'users.csv',
    Tags: 'tags.csv'
}

# А сюда прописать функцию обработки импорта.
LOAD_FUNCTIONS = {
    Ingredients: load_ingredients,
    User: load_users,
    Tags: load_tags
}


def wait_for_confirmation(sec):
    """Ожидание и возможность отмены действия."""

    for i in range(sec, 0, -1):
        sys.stdout.write(str(i) + ' ')
        sys.stdout.flush()
        time.sleep(1)


def load_func(self, *args, **options):
    """Загрузка данных в БД."""

    self.stdout.write(self.style.WARNING(
        'Перед загрузкой тестовых данных БД будет очищена. '
        'Чтобы отменить операцию импорта нажмите Ctrl + C'
    ))
    wait_for_confirmation(7)

    for model, file_csv in CSV_DATA.items():
        with open(
                f'{BASE_DIR}/data/{file_csv}',
                'r', encoding='utf-8'
        ) as file:
            data = csv.reader(file)

            if model in LOAD_FUNCTIONS:
                lst = LOAD_FUNCTIONS[model](data)

                # очищаем базу от старых данных перед импортом
                model.objects.all().delete()
                # наполняем новыми данными
                model.objects.bulk_create(lst)

                print(f'Файл "{file_csv}" загружен')
