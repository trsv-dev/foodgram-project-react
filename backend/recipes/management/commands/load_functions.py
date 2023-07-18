from recipes.models import Ingredients, User


def load_ingredients(data):
    """Функция для загрузки ингредиентов."""

    lst = []
    for row in data:
        name, measurement_unit = row
        ingredients = Ingredients(
            name=name, measurement_unit=measurement_unit
        )
        lst.append(ingredients)

    return lst


def load_users(data):
    """Функция для загрузки пользователей."""

    lst = []
    for row in data:
        email, username, first_name, last_name, role = row
        if username and email:
            user = User(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                role=role
            )
            lst.append(user)

    return lst
