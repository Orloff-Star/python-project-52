#!/usr/bin/env bash
# Установка uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Установка зависимостей, сборка статики, применение миграций
uv pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate