.PHONY: train run actions tensorboard clean interactive prepare release valid
train:
	NUMEXPR_MAX_THREADS=16 rasa train -d data

run:
	rasa run --enable-api --cors "*" --endpoints ./dev-config/endpoints.yml --credentials ./dev-config/credentials.yml
	#RASA_TELEMETRY_ENABLED=false  SANIC_WORKERS=5 ACTION_SERVER_SANIC_WORKERS=5 --debug

actions:
	rasa run actions --auto-reload

tensorboard:
	tensorboard --logdir ./tensorboard

clean:
	rm -rf models/
	rm -Rf .rasa

interactive:
	rasa interactive -d data

prepare:
	python -m spacy download zh_core_web_sm

release:
	docker build -t ccr.ccs.tencentyun.com/megalab/ops-pilot .
	docker push ccr.ccs.tencentyun.com/megalab/ops-pilot

valid:
	rasa data split nlu -u data/
	rasa test nlu --nlu data/   #--cross-validation --config config_1.yml config_2.yml --runs 4 --percentages 0 25 50 70 90