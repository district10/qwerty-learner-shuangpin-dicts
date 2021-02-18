all:
	time make dicts
	time make csv

lint:
	python3 -m yapf -ir . # -vv

dicts: large_pinyin.txt
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
	make sample1
	make sample2
	make sample3
	make sample4
sample1:
	python3 hanzi_freq.py --input source/sample1.txt --output-dict dicts/ziranma/sample1.json
sample2:
	python3 hanzi_freq.py --input source/sample2.txt --output-dict dicts/ziranma/sample2.json
sample3:
	python3 hanzi_freq.py --input source/sample3.txt --output-dict dicts/ziranma/sample3.json
sample4:
	python3 hanzi_freq.py --input source/sample4.txt --output-dict dicts/ziranma/sample4.json
zhihu:
	python3 hanzi_freq.py --input raw_source/zhihu.txt  --output-dict dicts/ziranma/zhihu.json
wiki:
	python3 hanzi_freq.py --input sample.txt --output-dict dicts/ziranma/wiki.json
.PHONY: dicts douban notes samples zhihu wiki

large_pinyin.txt:
	wget https://raw.githubusercontent.com/mozillazg/phrase-pinyin-data/22ed9d35cfb5ca5d8dbbea60938becafd9efa238/large_pinyin.txt

csv:
	python3 archiver.py \
		--input \
			../blog/notes/notes/*.md \
			raw_source/douban.txt  \
			raw_source/zhihu.txt \
			sample.txt \
			source/sample*.txt \
		--output-csv pinyin-shuangpin.csv
