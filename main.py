import pypinyin
from pyhanlp import *
import re

pinyin2shengyun_cache = {
    'a': ['a', 'a'],
    'o': ['o', 'o'],
    'e': ['e', 'e'],
    'ai': ['a', 'i'],
    'an': ['a', 'n'],
    'ao': ['a', 'o'],
    'ei': ['e', 'i'],
    'en': ['e', 'n'],
    'er': ['e', 'r'],
    'ou': ['o', 'u'],
    'ang': ['a', 'h'],
    'eng': ['e', 'g'],
}

def pinyin2shengyun(pinyin):
    if pinyin in pinyin2shengyun_cache:
        return pinyin2shengyun_cache[pinyin]
    shengs = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'w', 'x', 'y', 'z', 'ch', 'sh', 'zh'] 
    yuns = ['a', 'ai', 'an', 'ang', 'ao', 'e', 'ei', 'en', 'eng', 'i', 'ia', 'ian', 'iang', 'iao', 'ie', 'iong', 'in', 'ing', 'iu', 'o', 'ong', 'ou', 'u', 'ua', 'uai', 'uan', 'uang', 'ue', 'ui', 'un', 'uo', 'v', 've']
    for yun in yuns:
        if not pinyin.endswith(yun):
            continue
        idx = len(pinyin) - len(yun)
        sheng = pinyin[:idx]
        if sheng not in shengs:
            continue
        # print(f'{pinyin} -> {sheng},{yun}')
        pinyin2shengyun_cache[pinyin] = [sheng, yun]
    return pinyin2shengyun_cache[pinyin]


def hanzi2keys(line, *, shuangpin_mode=None):
    line = re.sub('[\u0000-\u007f]', '', line)
    keys = []
    for c in line:
        try:
            pinyin = pypinyin.pinyin(c, style=pypinyin.Style.NORMAL, errors='ignore')[0][0]
            sheng, yun = pinyin2shengyun(pinyin)
            keys.extend([sheng, yun])
        except Exception:
            pass
    if shuangpin_mode is None:
        return keys
    return keys


if __name__ == '__main__':
    print(hanzi2keys('我是中国人'))
