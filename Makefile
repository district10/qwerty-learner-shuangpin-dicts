all:
	@echo nothing special

lint:
	python3 -m yapf -ir . # -vv

notes:
	python3 hanzi_freq.py --input ../blog/notes/notes/*.md  --output-dict dicts/ziranma/notes.json

sample:
	python3 hanzi_freq.py --input sample.txt --output-dict sample.json
