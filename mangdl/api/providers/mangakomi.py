from ..base import soup, urel

scanlator = "Manga Komi"
base_url = "https://mangakomi.com"
template = "wordpress"

ch_num_fn = "wmcc"
src = "data-src"

def rch_fn(url):
    url = f"{base_url}/manga/{urel(url).parts[2]}/ajax/chapters/"
    return soup(url, method="post")