.PHONY: train run actions test clean

train:
	rasa train -d domain

run:
	rasa run --enable-api --cors "*"

actions:
	rasa run actions --auto-reload

test:
	rasa test

clean:
	rm -rf models/
	rm -Rf .rasa

interactive:
    rasa interactive

prepare:
    python -m spacy download zh_core_web_sm