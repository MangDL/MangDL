from ast import literal_eval

from ..base import soup, urel

scanlator = "Manga Komi"
base_url = "https://mangakomi.com"
template = "wordpress"

src = "data-src"

def ch_num_fn(soup):
    return literal_eval(".".join(soup.select_one("#wp-manga-current-chap")["value"].split("-")[1:]))

def rch_num_fun(url):
    return literal_eval(".".join(urel(url).parts[3].split("-")[1:]))

def rch_fn(url):
    url = f"{base_url}/manga/{urel(url).parts[2]}/ajax/chapters/"
    return soup(url, method="post")