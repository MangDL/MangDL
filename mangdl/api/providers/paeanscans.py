from ast import literal_eval

from ..base import urel

scanlator = "Paean Scans"
base_url = "https://paeanscans.com"
template = "wordpress"

rch_fn = "setsu"
rpa = 10

def ch_num_fn(soup):
    return literal_eval(".".join(soup.select_one("#chapter-heading").text.split("-")[1:]))

def rch_num_fn(url):
    return literal_eval(urel(url).parts[3].replace("-", "."))

def manga_id_fn(soup) -> str:
    cdata = soup.select_one("#wp-manga-js-extra").text
    return literal_eval(cdata[29:-12])["manga_id"]