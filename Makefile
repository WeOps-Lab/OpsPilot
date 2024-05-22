install:
	pip-compile -v
	pip-sync -v

venv-install:
	./.venv/bin/pip-compile -v
	./.venv/bin/pip-sync

train:
	NUMEXPR_MAX_THREADS=16 rasa train --domain ./configs/basic/data --data ./configs/basic/data -c ./configs/basic/config.yml --fixed-model-name ops-pilot

shell:
	rasa shell --endpoints ./configs/endpoints.yml --credentials ./configs/credentials.yml

run:
    RASA_TELEMETRY_ENABLED=false rasa run --enable-api --cors "*" --endpoints ./configs/endpoints.yml --credentials ./configs/credentials.yml

actions:
	rasa run actions --auto-reload

tensorboard:
	tensorboard --logdir ./tensorboard

interactive:
	rasa interactive -d data/dev -m models/ops-pilot.tar.gz

release:
	docker build -t ccr.ccs.tencentyun.com/megalab/ops-pilot .
	docker push ccr.ccs.tencentyun.com/megalab/ops-pilot

valid:
	rasa data split nlu -u data/
	rasa test nlu --nlu data/   #--cross-validation --config config_1.yml config_2.yml --runs 4 --percentages 0 25 50 70 90

finetune:
	NUMEXPR_MAX_THREADS=16 rasa train --finetune  -d data --fixed-model-name ops-pilot --epoch-fraction 0.5

visualize:
	rasa visualize -d ./configs/bert/data

DOC_IMAGE_NAME ?= ops-pilot-doc:latest
.PHONY: build-doc
build-doc:
	cd docs/site && docker build . -t $(DOC_IMAGE_NAME)

.PHONY: push-doc
push-doc: build-doc
	docker push $(DOC_IMAGE_NAME)