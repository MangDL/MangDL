import re
from ast import literal_eval

from ..base import urel

scanlator = "manga ZUKI"
base_url = "https://mangazuki.me"
template = "wordpress"

total_cs = ".c-blog__heading h4"

rchnfp = re.compile(r"[0-9]+(-[0-9])*")

def ch_num_fn(soup):
    return literal_eval(soup.select_one("ol.breadcrumb .active").text.split()[-1])

def rch_num_fun(url):
    parts = urel(url).parts
    op = rchnfp.search(parts[3]).group().replace("-", ".")
    return literal_eval(op)