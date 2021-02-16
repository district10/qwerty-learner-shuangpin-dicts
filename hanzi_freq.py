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
from main import hanzi2keys
import numpy as np
import random


def count_words(line: str, *, counter: Dict[str, int]):
    segments = HanLP.segment(line)
    for seg_idx, seg in enumerate(segments):
        seg = str(seg)
        idx = seg.rfind('/')
        hanzi = seg[:idx]
        counter[hanzi] += 1


if __name__ == '__main__':
    prog = 'hanzi frequency counter'
    description = ('count hanzi words frequency')
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument(
        '--input',
        type=str,
        nargs='+',
        help='input text file',
    )
    parser.add_argument(
        '--output-dict',
        type=str,
        help='output dict file (for qwerty-learner)',
    )
    parser.add_argument(
        '--output-frequency',
        type=str,
        help='output frequency file',
    )
    args = parser.parse_args()
    input_paths: List[str] = args.input
    output_dict_path: str = args.output_dict or tempfile.mktemp(suffix='.json')
    output_freq_path: str = args.output_frequency or tempfile.mktemp(suffix='.json')
    args = None

    counter = defaultdict(int)
    for path in input_paths:
        with open(path) as f:
            if path.endswith('.json'):
                print(f'loading frequence file from {path}...')
                for word, count in json.load(f).items():
                    if isinstance(count, int) and count > 0:
                        counter[word] += count
            else:
                print(f'loading text file from {path}...')
                lines = f.readlines()
                for line in tqdm(lines, f'counting words of #{len(lines):,} lines...'):
                    count_words(line, counter=counter)
    for key in list(counter.keys()):
        if not len(re.findall(r'[\u4e00-\u9fff]', key)):
            counter.pop(key, None)
    # pprint(counter)
    freq2word = sorted([(v, k) for k, v in counter.items()], key=cmp_to_key(lambda kv1, kv2: kv2[0] - kv1[0]))
    counter = OrderedDict()
    for freq, word in freq2word:
        counter[word] = freq
    # pprint(counter)

    if not output_freq_path:
        output_freq_path = tempfile.mktemp(suffix='.json')
    output_freq_path = os.path.abspath(output_freq_path)
    os.makedirs(os.path.dirname(output_freq_path), exist_ok=True)
    with open(output_freq_path, 'w') as f:
        json.dump(counter, f, indent=4, ensure_ascii=False)
    print(f'wrote to {output_freq_path}')

    output_dict_path = os.path.abspath(output_dict_path)
    os.makedirs(os.path.dirname(output_dict_path), exist_ok=True)
    with open(output_dict_path, 'w') as f:
        upper_thresh = list([i[0] for i in freq2word])[10] # select a big freq
        items = [{
            'name': ''.join(hanzi2keys(w, shuangpin_schema='ziranma')),
            'trans': [w, c, int(np.log(min(c, upper_thresh))) + 1],
        } for w, c in counter.items()]
        ret = []
        for i in items:
            ret.extend([i] * i['trans'][-1])
        for N in [50, 100, 300]:
            for k in list(range(len(ret) // N)):
                i, j = k * N, (k+1) * N
                copy = list(ret[i:j])
                random.shuffle(copy)
                ret[i:j] = copy
        json.dump(ret, f, indent=4, ensure_ascii=False)
    print(f'wrote to {output_dict_path}')
