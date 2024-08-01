setup:
	pip install pip-tools

venv-install:
	./.venv/bin/pip-compile -v
	./.venv/bin/pip-sync

migrate:
	python manage.py makemigrations
	python manage.py migrate

clean-migrate:
	cd apps &&\
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete &&\
	find . -path "*/migrations/*.pyc"  -delete

setup-sample-data:
	DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_EMAIL=admin@example.com DJANGO_SUPERUSER_PASSWORD=password python manage.py createsuperuser --noinput

init-data:
	python manage.py init_llm
	python manage.py init_channel
	python manage.py init_bot

run:
	daphne -b 0.0.0.0 -p 8000 munchkin.asgi:application

collectstatic:
	python manage.py collectstatic --noinput

init-buckets:
	python manage.py initialize_buckets

celery:
	celery -A munchkin worker -B --loglevel=info --pool threads

celery-inspect:
	celery -A munchkin inspect scheduled

celery-flower:
	celery -A munchkin flower

download_models:
	git clone https://huggingface.co/maidalun1020/bce-embedding-base_v1