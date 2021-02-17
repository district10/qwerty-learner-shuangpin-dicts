from os.path import basename
import pypinyin
from typing import Union, Set, Dict, List, Any, Tuple, Optional
import re
import json
from pprint import pprint
import os
import glob
from tqdm import tqdm
from pyhanlp import *

PWD = os.path.abspath(os.path.dirname(__file__))
SOURCE_DIR = f'{PWD}/source'
DICTS_DIR = f'{PWD}/dicts'


PATCHED_PINYIN_DICT: bool = False
def patch_pinyin_dict():
    global PATCHED_PINYIN_DICT
    if PATCHED_PINYIN_DICT:
        return
    phrases = {}
    with open(f'{PWD}/large_pinyin.txt') as f:
        lines = f.readlines()
        for line in tqdm(lines):
            cols = line.split(': ')
            if len(cols) != 2:
                continue
            hanzi = cols[0]
            pinyin = cols[1].split()
            if len(hanzi) != len(pinyin):
                print(f'skip line {line}')
                continue
            phrases[hanzi] = [[p] for p in pinyin]
    pypinyin.load_phrases_dict(phrases)
    PATCHED_PINYIN_DICT = True


PINYIN2SHENGYUN_CACHE: Dict[str, Tuple[str, str]] = {
    # TODO, fix 零声母方案
    'a': ('a', 'a'),
    'o': ('o', 'o'),
    'e': ('e', 'e'),
    'ai': ('a', 'i'),
    'an': ('a', 'n'),
    'ao': ('a', 'o'),
    'ei': ('e', 'i'),
    'en': ('e', 'n'),
    'er': ('e', 'r'),
    'ou': ('o', 'u'),
    'ang': ('a', 'h'),
    'eng': ('e', 'g'),
}

def pinyin2shengyun(pinyin: str) -> Union[Tuple[str, str], str]:
    global PINYIN2SHENGYUN_CACHE
    if pinyin in PINYIN2SHENGYUN_CACHE:
        return PINYIN2SHENGYUN_CACHE[pinyin]
    shengs = [
        'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r',
        's', 't', 'w', 'x', 'y', 'z', 'ch', 'sh', 'zh'
    ]
    yuns = [
        'a', 'ai', 'an', 'ang', 'ao', 'e', 'ei', 'en', 'eng', 'i', 'ia', 'ian',
        'iang', 'iao', 'ie', 'iong', 'in', 'ing', 'iu', 'o', 'ong', 'ou', 'u',
        'ua', 'uai', 'uan', 'uang', 'ue', 'ui', 'un', 'uo', 'v', 've'
    ]
    for yun in yuns:
        if not pinyin.endswith(yun):
            continue
        idx = len(pinyin) - len(yun)
        sheng = pinyin[:idx]
        if sheng not in shengs:
            continue
        PINYIN2SHENGYUN_CACHE[pinyin] = (sheng, yun)
        return PINYIN2SHENGYUN_CACHE[pinyin]
    return pinyin


SHUANGPIN_SCHEMAS: Optional[Dict[str, Dict]] = None


def get_schema(schema: Optional[str] = None) -> Union[Dict, List[str]]:
    global SHUANGPIN_SCHEMAS
    if not SHUANGPIN_SCHEMAS:
        with open(f'{SOURCE_DIR}/shuangpin.json') as f:
            shuangpin = json.load(f)
            SHUANGPIN_SCHEMAS = {s['id']: s for s in shuangpin['schemas']}
    if not schema:
        return list(SHUANGPIN_SCHEMAS.keys())
    return SHUANGPIN_SCHEMAS[schema]


def segmentize(line: str):
    segments = [str(s) for s in HanLP.segment(line)]
    words = [s[:s.rfind('/')] for s in segments]
    hanzis = [re.sub('[\u0000-\u007f]', '', w) for w in words]
    return [h for h in hanzis if h]


def hanzi2keys(line, *, shuangpin_schema=None):
    patch_pinyin_dict()
    keys = []
    for word in segmentize(line):
        try:
            pinyins = pypinyin.pinyin(word, style=pypinyin.Style.NORMAL, errors='ignore')
            for pinyin in [py[0] for py in pinyins]:
                shengyun = pinyin2shengyun(pinyin)
                if isinstance(shengyun, str):
                    keys.append(shengyun)
                else:
                    keys.extend(shengyun)
        except Exception as e:
            print(repr(e))
    if shuangpin_schema is None or shuangpin_schema not in get_schema():
        return keys
    schema = get_schema(shuangpin_schema)
    assert isinstance(schema, dict)
    sheng = schema['detail']['sheng']
    yun = schema['detail']['yun']
    other = schema['detail']['other']
    for i, k in enumerate(keys):
        if k in sheng:
            keys[i] = sheng[k]
        elif k in yun:
            keys[i] = yun[k]
        elif k in other:
            keys[i] = other[k]
    # e.g. ue->[t,v] ===> ue->t
    return [k if isinstance(k, str) else k[0] for k in keys]


if __name__ == '__main__':


    for text in [
        '似乎',
        '类似',
        '帧率',
        '命令行',
        '我是中国人',
        '我是中 国人',
        '这是一个矩阵 Matrix 队列 / yes',
    ]:
        print()
        print('文本:', text)
        print('分词:', segmentize(text))
        print('拼音:', hanzi2keys(text))
        print('双拼:', hanzi2keys(text, shuangpin_schema='ziranma'))