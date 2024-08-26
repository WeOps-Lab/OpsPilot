push:
	git add . && codegpt commit . && git push

update-submodules:
	git pull --recurse-submodules
	git submodule update --init --recursive
	git submodule update --remote --merge
	