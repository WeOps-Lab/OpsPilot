.PHONY: setup install venv-install train run shell actions tensorboard interactive release valid

setup:
	pip install pip-tools

download-kscan:
	mkdir -p ./libs/kscan &&\
	cd ./libs/kscan &&\
	wget -c "https://github.com/lcvvvv/kscan/releases/download/v1.85/kscan_linux_amd64.zip" &&\
	unzip kscan_linux_amd64.zip &&\
	mv kscan_linux_amd64 kscan &&\
	chmod +x kscan &&\
	./kscan --download-qqwry &&\
	rm -Rf kscan_linux_amd64.zip

install:
	pip-compile
	pip-sync

venv-install:
	./.venv/bin/pip-compile -v
	./.venv/bin/pip-sync

train:
	NUMEXPR_MAX_THREADS=16 rasa train --domain data --fixed-model-name ops-pilot

run:
	RASA_TELEMETRY_ENABLED=false rasa run --enable-api --cors "*" --endpoints ./endpoints.yml --credentials ./credentials.yml
	#SANIC_WORKERS=5 ACTION_SERVER_SANIC_WORKERS=5 --debug

dev:
	RASA_TELEMETRY_ENABLED=false rasa run --enable-api --cors "*" --endpoints ./endpoints-dev.yml --credentials ./credentials-dev.yml

shell:
	rasa shell

actions:
	rasa run actions --auto-reload

tensorboard:
	tensorboard --logdir ./tensorboard

interactive:
	rasa interactive -d data -m models/ops-pilot.tar.gz

release:
	docker build -t ccr.ccs.tencentyun.com/megalab/ops-pilot .
	docker push ccr.ccs.tencentyun.com/megalab/ops-pilot

valid:
	rasa data split nlu -u data/
	rasa test nlu --nlu data/   #--cross-validation --config config_1.yml config_2.yml --runs 4 --percentages 0 25 50 70 90

finetune:
	NUMEXPR_MAX_THREADS=16 rasa train --finetune  -d data --fixed-model-name ops-pilot --epoch-fraction 0.5

visualize:
	rasa visualize -d data

celery:
	celery -A tasks.celery worker --loglevel=INFO

DOC_IMAGE_NAME ?= ops-pilot-doc:latest
.PHONY: build-doc
build-doc:
	cd docs/site && docker build . -t $(DOC_IMAGE_NAME) 

.PHONY: push-doc
push-doc: build-doc
	docker push $(DOC_IMAGE_NAME)