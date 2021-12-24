from timeit import timeit

import_module = "import re"
testcode = r'''
string = 'how much for the maple syrup? $20.99? That s ridiculous!!!'
re.sub('\W+','', string)
'''
print(timeit(stmt=testcode, setup=import_module))