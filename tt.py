from timeit import timeit

import_module = r"""
import unicodedata
import regex as re
import itertools
import sys
all_chars = (chr(i) for i in range(sys.maxunicode))
categories = {'Cc'}
control_chars = ''.join(c for c in all_chars if unicodedata.category(c) in categories)
control_chars = ''.join(map(chr, itertools.chain(range(0x00,0x20), range(0x7f,0xa0))))
control_char_re = re.compile('[%s]' % re.escape(control_chars))
def clean(s: str):
    return control_char_re.sub('', s)
"""
testcode = r'''
clean("\t\t\t\ngadads\x02\x03sadda\x10\x11\x12fsadfsdfsdd")
'''
print(timeit(stmt=testcode, setup=import_module))