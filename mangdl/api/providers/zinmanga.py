from ast import literal_eval

from ..base import urel

scanlator = "Zinmanga"
base_url = "https://zinmanga.com"
template = "wordpress"

src = "data-src"

def ch_num_fn(soup):
    return literal_eval(soup.select_one("ol.breadcrumb .active").text.split()[-1])

def rch_num_fun(url: str):
    return literal_eval(".".join(urel(url).parts[3].split("-")[1:]))