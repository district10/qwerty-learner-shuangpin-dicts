import pypinyin
from pyhanlp import *
from typing import Union, Set, Dict, List, Any, Tuple, Optional
import re
import json
from pprint import pprint

PWD = os.path.abspath(os.path.dirname(__file__))
SOURCE_DIR = f'{PWD}/source'

PINYIN2SHENGYUN_CACHE: Dict[str, Tuple[str, str]] = {}


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


def hanzi2keys(line, *, shuangpin_schema=None):
    line = re.sub('[\u0000-\u007f]', '', line)
    keys = []
    for c in line:
        try:
            pinyin = pypinyin.pinyin(
                c, style=pypinyin.Style.NORMAL, errors='ignore')[0][0]
            shengyun = pinyin2shengyun(pinyin)
            if isinstance(shengyun, str):
                keys.append(shengyun)
            else:
                keys.extend(shengyun)
        except Exception:
            pass
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
    return keys


if __name__ == '__main__':
    print('我是中国人')
    print(hanzi2keys('我是中国人'))
    print(hanzi2keys('我是中国人', shuangpin_schema='ziranma'))

    shuangpin_schema = 'ziranma'
    ret = []
    with open(f'{SOURCE_DIR}/sample1.txt') as f:
        for raw_line in f.readlines():
            raw_line = raw_line.strip()
            line = re.sub('[\u0000-\u007f]', '', raw_line)
            if not line:
                continue
            keys = hanzi2keys(line, shuangpin_schema=shuangpin_schema)
            ret.append({
                'name': ''.join(keys),
                'trans': [raw_line],
            })
    pprint(ret)
