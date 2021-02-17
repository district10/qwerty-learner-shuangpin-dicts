from pyhanlp import *
from typing import DefaultDict, OrderedDict, Union, Set, Dict, List, Any, Tuple, Optional
from collections import defaultdict
from pprint import pprint
import argparse
import json
import re
from functools import cmp_to_key
from tqdm import tqdm
import tempfile
from main import segmentize, hanzi2keys

if __name__ == '__main__':
    prog = 'pinyn & shuangpin of every words'
    description = ('archiver')

    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument(
        '--input',
        type=str,
        nargs='+',
        help='input text file',
    )
    parser.add_argument(
        '--output-csv',
        type=str,
        required=True,
        help='output csv file',
    )
    args = parser.parse_args()
    input_paths: List[str] = args.input
    output_csv_path: str = os.path.abspath(args.output_csv)
    args = None

    words = set()
    for path in input_paths:
        print(f'loading {path}...')
        with open(path) as f:
            lines = f.readlines()
            for line in tqdm(lines):
                words.update(segmentize(line))
    words = sorted(words)
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    with open(output_csv_path, 'w') as f:
        for i, w in enumerate(words):
            pinyin = hanzi2keys(w)
            if not pinyin:
                continue
            ziranma = hanzi2keys(w, shuangpin_schema='ziranma')
            f.write(f'{w}, {pinyin}, {ziranma}\n')
    print(f'wrote to {output_csv_path}')