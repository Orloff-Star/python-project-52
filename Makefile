build:
	./build.sh

lint:
	poetry run flake8 task_manager

compilemessages:
	django-admin compilemessages

makemessages:
	django-admin makemessages -l ru

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

install:
	poetry install

dev:
	poetry run python manage.py runserver

start:
	poetry run gunicorn -w 2 -b 0.0.0.0:8000 task_manager.wsgi

test:
	poetry run ./manage.py test
