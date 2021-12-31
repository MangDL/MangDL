from ast import literal_eval

from ..base import soup, urel

scanlator = "vinmanga"
base_url = "https://vinload.com"
template = "wordpress"

def ch_num_fn(soup):
    return literal_eval(soup.select_one("ol.breadcrumb .active").text.split()[-1])

def rch_num_fun(url: str):
    return literal_eval(".".join(urel(url).parts[3].split("-")[1:]))

def rch_fn(url):
    url = f"{base_url}/manga/{urel(url).parts[2]}/ajax/chapters/"
    return soup(url, method="post")