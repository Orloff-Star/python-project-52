build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

lint:
	poetry run flake8 task_manager

compilemessages:
	django-admin compilemessages

makemessages:
	django-admin makemessages --ignore="static" --ignore=".env" -l en

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate