from ast import literal_eval

cloudflare = True

scanlator = "1ST Kiss MANGA"
base_url = "https://1stkissmanga.io"
template = "wordpress"

rch_fn = "setsu"

def ch_num_fn(soup):
    return literal_eval(".".join(soup.select_one("#wp-manga-current-chap")["value"].split("-")[1:]))

def manga_id_fn(soup) -> str:
    cdata = soup.select_one("#wp-manga-js-extra").text
    return literal_eval(cdata[29:-12])["manga_id"]