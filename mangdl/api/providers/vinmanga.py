from ..base import soup, urel

scanlator = "vinmanga"
base_url = "https://vinload.com"
template = "wordpress"

def rch_fn(url):
    url = f"{base_url}/manga/{urel(url).parts[2]}/ajax/chapters/"
    return soup(url, method="post")