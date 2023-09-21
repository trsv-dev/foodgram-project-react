## **Сайт Foodgram, «Продуктовый помощник».**

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)

### Онлайн-сервис и API. 

На этом сервисе пользователи могут 
публиковать рецепты, подписываться на публикации других пользователей, 
добавлять понравившиеся рецепты в список «Избранное», а перед походом в 
магазин скачивать сводный список продуктов, необходимых для приготовления 
одного или нескольких выбранных блюд.

![img.png](img.png)

#### Технологи:

- Python 3.9
- Django 3.2.3
- Django Rest Framework 3.12.4
- Djoser 2.2.0
- Gunicorn 20.1.0

#### Серверная инфраструктура:
- Docker
- PostgresSQL
- Nginx
- GitHub Actions
- Linux Ubuntu с публичным IP

### Предварительные настройки:

**_Подразумевается, что Docker уже установлен на локальной машине._**

- Клонируем репозиторий: 
```
git clone git@github.com:trsv-dev/foodgram-project-react.git
```
- Переходим в папку **infra**:
```
cd foodgram-project-react/infra/
```
- В ней создаем файл **.env** и заполняем его по примеру **.env.example**:
```
#Django settings:
###############################################################################
DEBUG=True
SECRET_KEY=my_superduper_strong_django_secret_key
ALLOWED_HOSTS=127.0.0.1, localhost

#PostgreSQL settings:
###############################################################################
POSTGRES_DB=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram_password
DB_NAME=foodgram
DB_HOST=db
DB_PORT=5432

#Nginx settings:
###############################################################################
NGINX_PORT=80

#DockerHub settings:
###############################################################################
DOCKERHUB_LOGIN=your_dockerhub_login
```

### Билдим образы и запускаем (локально):

```
# В директории infra...

# запускаем сборку
docker compose -f docker-compose.yml up -d

# делаем миграции
docker compose -f docker-compose.yml exec backend python manage.py migrate

# загружаем тестовые данные
docker compose -f docker-compose.yml exec backend python manage.py load_csv

# создаем суперпользователя
docker compose -f docker-compose.yml exec backend python manage.py createsuperuser

# собираем статику
docker compose -f docker-compose.yml exec backend python manage.py collectstatic

# раскладываем статику по местам
docker compose -f docker-compose.yml exec backend cp -r /app/collected_static/. /app/static/
```
Проверьте, что на вашем компьютере созданы необходимые образы, 
— выполните команду `docker image ls`.

Проверяем работу. Заходим на http://127.0.0.1:80

### Разворачиваем на сервере:
_**Подразумевается, что Docker уже установлен на сервере.**_

Копируем на сервер содержимое папки **infra** и если .env был до этого заполнен актуальными данными, то просто запускаем:
```
docker compose -f docker-compose.production.yml up -d
```
Дожидаемся окончания развертывания и проверяем работу. Заходим на [http://ваш_домен_в_ALLOWED_HOSTS]()