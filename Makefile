build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

lint:
	poetry run flake8 task_manager
