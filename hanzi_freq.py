from pyhanlp import *
from typing import DefaultDict, OrderedDict, Union, Set, Dict, List, Any, Tuple, Optional
from collections import defaultdict
from pprint import pprint
import argparse
import json
import re
from functools import cmp_to_key


def count_words(line: str, *, counter: Dict[str, int]):
    segments = HanLP.segment(line)
    for seg_idx, seg in enumerate(segments):
        seg = str(seg)
        idx = seg.rfind('/')
        hanzi = seg[:idx]
        counter[hanzi] += 1


if __name__ == '__main__':
    # sys.argv = 'hanzi_freq.py --input source/sample2.txt'.split()

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
    output_dict_path: Optional[str] = args.output_dict
    output_freq_path: Optional[str] = args.output_frequency
    args = None

    counter = defaultdict(int)
    for path in input_paths:
        with open(path) as f:
            for line in f.readlines():
                count_words(line, counter=counter)
    for key in list(counter.keys()):
        if not len(re.findall(r'[\u4e00-\u9fff]', key)):
            counter.pop(key, None)
    # pprint(counter)
    freq2word = sorted([(v, k) for k, v in counter.items()], key=cmp_to_key(lambda kv1, kv2: kv2[0] - kv1[0]))
    counter = OrderedDict()
    for freq, word in freq2word:
        counter[word] = freq
    pprint(counter)

    if output_freq_path:
        output_freq_path = os.path.abspath(output_freq_path)
        os.makedirs(os.path.dirname(output_freq_path), exist_ok=True)
        with open(output_freq_path, 'w') as f:
            json.dump(counter, f, indent=4, ensure_ascii=False)
        print(f'wrote to {output_freq_path}')

    if output_dict_path:
        output_dict_path = os.path.abspath(output_dict_path)
        os.makedirs(os.path.dirname(output_dict_path), exist_ok=True)
        pass
