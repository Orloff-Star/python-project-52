build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

lint:
	poetry run flake8 task_manager

compilemessages:
	django-admin compilemessages

makemessages:
	django-admin makemessages -l ru

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate