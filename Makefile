train:
	rasa train -d data

run:
	rasa run --enable-api --cors "*" --debug
	#SANIC_WORKERS=5 ACTION_SERVER_SANIC_WORKERS=5


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
