import ast
import urllib
from typing import Any, Callable, Dict, List, Union

from ...utils.utils import dt, sanitize_text
from ..base import Ch, Downloader, Manga, Search, soup, urel


def chapter(url: str) -> Ch:
    ms = soup(url)
    ch = ms.select_one("#wp-manga-current-chap")["value"].split("-")[-1]
    return Ch(
        url              = url,
        ch               = ch,
        vol              = None,
        title            = f"Chapter {ch}",
        scanlator_groups = "Mangasushi",
        imgs             = [sanitize_text(i["data-src"]) for i in ms.select(".page-break img")],
    )

def manga(url: str, chs: int=0) -> Manga:
    ms = soup(url)
    meta = {}
    for c in ["post-content_item", "post-status"]:
        for m in ms.select(f"div.{c}"):
            v = m.select_one(".summary-content")
            idx = sanitize_text(m.select_one("h5").text)
            if v:
                meta[idx] = sanitize_text(v.text)
            else:
                meta[idx] = [sanitize_text(i.text) for i in m.select("a")]

    def mst(s: str, pp: Callable[[str], List[Any]]=lambda x: x):
        return pp(sanitize_text(meta.get(s))) if meta.get(s) else []

    rch = soup(f"https://mangasushi.net/manga/{urel(url).parts[2]}/ajax/chapters/", method="post")
    dates = [sanitize_text(i.text) for i in rch.select(".chapter-release-date")]
    chap_dict={}
    if chs:
        for c in rch.select("li.wp-manga-chapter    a"):
            cch = c["href"]
            if chs == 2:
                cch = chapter(cch)
            chap_dict[ast.literal_eval(urel(c["href"]).parts[3].split("-")[-1])] = cch
    return Manga(
        url             = url,
        covers          = [ms.select_one(".summary_image img")["src"]],
        title           = sanitize_text(ms.select_one("div.post-title h1").text),
        alt_titles      = mst("Alternative"),
        author          = mst("Author(s)", lambda x: x.split(",")),
        artist          = mst("Artist(s)", lambda x: x.split(",")),
        status          = {k: v for v, k in enumerate(["OnGoing", "Completed", "On Hold"])}.get(meta["Status"], -1),
        genres          = mst("Genre(s)", lambda x: x.split(",")),
        updated_at      = dt(dates[0], r"%B %d, %Y") if dates else "1970-01-01T00:00:00",
        created_at      = dt(dates[-1], r"%B %d, %Y") if dates else "1970-01-01T00:00:00",
        description     = sanitize_text(ms.select_one(".summary__content").text),
        chapters        = chap_dict,
    )

def dl_search(title: str, **kwargs: Dict[str, Any]) -> Dict[str, str]:
    sr = {}
    def pr(num: int):
        url = f"https://mangasushi.net/page/{num}?s={urllib.parse.quote_plus(title)}&post_type=wp-manga"
        ts = soup(url).select("div.post-title a")
        for r in ts:
            if not r.select_one(".limit .novelabel"):
                sr[r.text] = r["href"]
        return len(ts)
    i = 1
    cp = pr(i)
    while cp // 12:
        i += 1
        cp = pr(i)
    return sr

def search(s: Search) -> List[Manga]:
    return [manga(i) for i in dl_search(**s.__dict__).values()]

def cli_search(title: str, **kwargs: Dict[str, Any]) -> Dict[str, str]:
    return dl_search(title, **kwargs)

def ch_fn(url: str) -> List[str]:
    op = [sanitize_text(i["data-src"]) for i in soup(url).select(".page-break img")]
    return op

def chdls(url: str) -> List[Dict[Union[float, int, None], str]]:
    op = []
    rch = soup(f"https://mangasushi.net/manga/{urel(url).parts[2]}/ajax/chapters/", method="post")
    for c in rch.select("li.wp-manga-chapter    a"):
        op.append({ast.literal_eval(urel(c["href"]).parts[3].split("-")[-1]): c["href"]})
    return op

def dl(url: str, **kwargs: Dict[str, Any]):
    ms = soup(url)
    Downloader(ch_fn, **kwargs).dl_chdls(chdls(url), sanitize_text(ms.select_one("div.post-title h1").text))

def cli_dl(title: str, **kwargs: Dict[str, Any]):
    Downloader(ch_fn, **kwargs).cli(cli_search, chdls, title)
