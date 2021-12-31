from ast import literal_eval

from ..base import soup, urel

scanlator = "Chibimanga"
base_url = "https://www.cmreader.info"
template = "wordpress"

src = "data-src"

def ch_num_fn(soup):
    return literal_eval(".".join(soup.select_one("#wp-manga-current-chap")["value"].split("-")[1:]))

def rch_num_fun(url):
    return literal_eval(".".join(urel(url).parts[3].split("-")[1:]))

def manga_id_fn(soup):
    return soup.select_one("#manga-chapters-holder")["data-id"]

def rch_fn(url):
    data = {"action": "manga_get_chapters", "manga": str(manga_id_fn(soup(url)))}
    return soup(f"{base_url}/wp-admin/admin-ajax.php", method="post", data=data)