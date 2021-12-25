import urllib
from typing import Any, Dict, List, Union

from ...utils.utils import dt
from ..base import Ch, Downloader, Manga, Search, soup, urel

user = ""

def chapter(url: str) -> Ch:
    global user
    ms = soup(url)
    ch = ms.select_one("h1.entry-title").text.split()[-1]
    if not user:
        slug = '-'.join(urel(url).parts[1].split('-')[:-2])
        us = soup(f"https://acescans.xyz/manga/{slug}")
        meta = {}
        for m in us.select(".tsinfo.bixbox .imptdt"):
            i = m.select_one("i")
            meta[m.next_element.strip()] = i.text if i else m.select_one("a").text
        user = meta["Posted By"]
    return Ch(
        url              = url,
        ch               = ch,
        vol              = None,
        title            = f"Chapter {ch}",
        scanlator_groups = "Ace Scans",
        user             = user,
        imgs             = [i["src"] for i in ms.select("#readerarea p img")],
    )

def manga(url: str, chs: int=0) -> Manga:
    global user
    ms = soup(url)
    meta = {}
    for m in ms.select(".tsinfo.bixbox .imptdt"):
        i = m.select_one("i")
        meta[m.next_element.strip()] = i.text if i else m.select_one("a").text

    chap_dict={}
    if chs:
        for c in ms.select("div.eplister ul li"):
            cch = c.select_one("a")["href"]
            if chs == 2:
                cch = chapter(cch)
            chap_dict[c["data-num"]] = cch

    user = meta["Posted By"]

    return Manga(
        url             = url,
        covers          = [ms.select_one(".thumb .attachment-.size-.wp-post-image")["src"]],
        title           = ms.select_one("h1.entry-title").text,
        alt_titles      = ms.select_one("span.alternative").text.split(" | "),
        author          = meta["Author"].split(", "),
        status          = {k: v for v, k in enumerate(["Ongoing", "Completed", "Hiatus", "Cancelled"])}.get(meta["Status"], -1),
        updated_at      = dt(meta["Updated On"], r"%B %d, %Y"),
        created_at      = dt(meta["Posted On"], r"%B %d, %Y"),
        description     = "\n".join(i.text for i in ms.select(".entry-content.entry-content-single p")),
        chapters        = chap_dict,
    )

def dl_search(title: str, **kwargs: Dict[str, Any]) -> Dict[str, str]:
    sr = {}
    ms = soup(f"https://acescans.xyz/?s={urllib.parse.quote_plus(title)}")
    pages = ms.select("a.page-numbers")
    if pages:
        for p in range(int(pages[-2].text)):
            for r in soup(f"https://acescans.xyz/page/{p+1}/?s={urllib.parse.quote_plus(title)}").select(".listupd .bs .bsx a"):
                sr[r["title"]] = r["href"]
    else:
        for r in ms.select(".listupd .bs .bsx a"):
            sr[r["title"]] = r["href"]
    return sr

def search(s: Search) -> List[Manga]:
    return [manga(i) for i in dl_search(**s.__dict__).values()]

def cli_search(title: str, **kwargs: Dict[str, Any]) -> Dict[str, str]:
    return dl_search(title, **kwargs)

def ch_fn(url: str) -> List[str]:
    return [i["src"] for i in soup(url).select("#readerarea p img")]

def chdls(url: str) -> List[Dict[Union[float, int, None], str]]:
    op = []
    for c in soup(url).select("div.eplister ul li"):
        op.append({c["data-num"]: c.select_one("a")["href"]})
    return op

def dl(url: str, **kwargs: Dict[str, Any]):
    ms = soup(url)
    Downloader(ch_fn, **kwargs).dl_chdls(chdls(url), ms.select_one("h1.entry-title").text)

def cli_dl(title: str, **kwargs: Dict[str, Any]):
    Downloader(ch_fn, **kwargs).cli(cli_search, chdls, title)
