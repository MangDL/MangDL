from ast import literal_eval

from mangdl.utils.utils import sanitize_text

from ..base import urel

scanlator = "Setsu Scans"
base_url = "https://setsuscans.com"
template = "wordpress"

cs_manga = "div.tab-summary"
rch_fn = "setsu"
src = "data-src"

def ch_num_fn(soup):
    return literal_eval(soup.select_one("#chapter-heading").text.split("-")[-1][9:])

def rch_num_fun(url: str):
    return literal_eval(".".join(urel(url).parts[3].split("-")[1:]))

def manga_id_fn(soup) -> str:
    return soup.select_one("#manga-chapters-holder")["data-id"]

def manga_check(soup):
    return not sanitize_text(soup.select_one(".mg_genres a").text) == "Bilibili"

def title_fn(soup):
    return soup.select_one(".post-title a").text

def link_fn(soup):
    return soup.select_one(".post-title a")["href"]