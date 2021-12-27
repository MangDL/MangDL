from ast import literal_eval

from ..base import soup, urel

scanlator = "Paean Scans"
base_url = "https://paeanscans.com"
template = "wordpress"

rch_fn = "setsu"
rpa = 10

def ch_num_fn(soup):
    return literal_eval(".".join(soup.select_one("#chapter-heading").text.split("-")[1:]))

def rch_num_fun(url):
    return literal_eval(urel(url).parts[3].replace("-", "."))

def manga_id_fn(soup) -> str:
    cdata = soup.select_one("#wp-manga-js-extra").text
    return literal_eval(cdata[29:-12])["manga_id"]

def rch_fn(url):
    data = {"action": "manga_get_chapters", "manga": str(manga_id_fn(soup(url)))}
    return soup(f"{base_url}/wp-admin/admin-ajax.php", method="post", data=data)