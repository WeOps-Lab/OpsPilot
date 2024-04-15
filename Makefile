.PHONY: setup install venv-install train run shell actions tensorboard interactive release valid

setup:
	pip install pip-tools

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

shell:
	rasa shell

actions:
	rasa run actions --auto-reload

tensorboard:
	tensorboard --logdir ./tensorboard

interactive:
	rasa interactive -d data

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