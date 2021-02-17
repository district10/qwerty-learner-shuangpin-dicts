all:
	time make dicts

lint:
	python3 -m yapf -ir . # -vv

dicts:
	make douban
	make notes
	make samples
	make wiki
	make zhihu
douban:
	python3 hanzi_freq.py --input raw_source/douban.txt  --output-dict dicts/ziranma/douban.json
notes:
	python3 hanzi_freq.py --input ../blog/notes/notes/*.md  --output-dict dicts/ziranma/notes.json
samples:
	python3 hanzi_freq.py --input source/sample1.txt --output-dict dicts/ziranma/sample1.json
	python3 hanzi_freq.py --input source/sample2.txt --output-dict dicts/ziranma/sample2.json
	python3 hanzi_freq.py --input source/sample3.txt --output-dict dicts/ziranma/sample3.json
zhihu:
	python3 hanzi_freq.py --input raw_source/zhihu.txt  --output-dict dicts/ziranma/zhihu.json
wiki:
	python3 hanzi_freq.py --input sample.txt --output-dict dicts/ziranma/wiki.json
.PHONY: dicts douban notes samples zhihu wiki
