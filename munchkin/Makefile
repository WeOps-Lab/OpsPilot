setup:
	pip install pip-tools

venv-install:
	./.venv/bin/pip-compile -v
	./.venv/bin/pip-sync

migrate:
	python manage.py makemigrations
	python manage.py migrate

setup-sample-data:
	DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_EMAIL=admin@example.com DJANGO_SUPERUSER_PASSWORD=password python manage.py createsuperuser --noinput

run:
	daphne -b 0.0.0.0 -p 8000 munchkin.asgi:application

collectstatic:
	python manage.py collectstatic --noinput