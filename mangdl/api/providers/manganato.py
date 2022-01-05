import ast
import re
from datetime import datetime
from typing import Any, Callable, Dict, List, Union

from ..base import Ch, Downloader, Manga, soup


def chapter(url):
    c = soup("/".join(url.split("/")[:-1])).select_one(f'a[href="{url}"]').find_parent()
    a = c.select_one("a")
    ch = a["href"].split("-")[-1]
    ch = ast.literal_eval(ch) if ch else ch
    return Ch(
        url             = url,
        ch              = ch,
        vol             = None,
        title           = a.text,
        views           = int(c.select_one("span.chapter-view.text-nowrap").text.replace(",", "")),
        uploaded_at     = str(datetime.strptime(c.select_one("span.chapter-time.text-nowrap")["title"], '%b %d,%Y %H:%M')),
        imgs            = [i["src"] for i in soup(url).select(".container-chapter-reader img")]
    )

def manga(url, chs=0):
    ms = soup(url)
    ti = [i["class"][0] for i in ms.select(".table-label i")]
    si = [i["class"][0] for i in ms.select(".stre-label i")]
    def info(key: str, l: Callable[[str], Any]=None, d: Any=None) -> Any:
        key = f"info-{key}"
        op = d
        if key in ti:
            op = ms.select(f'.variations-tableInfo tbody tr:nth-child({ti.index(key) + 1}) td')[1]
        elif key in si:
            op = ms.select(f'p:nth-child({si.index(key) + 1}) .stre-value')[0]
        return l(op) if l else d
    rc = ms.select("li.a-h")
    chap_dict = {}
    if chs:
        n = 1
        for c in rc:
            a = c.select_one("a")
            ch = a["href"].split("-")[-1]
            if ch:
                k = ast.literal_eval(ch)
            else:
                k = -n
                n += 1
            cch = a["href"]
            if chs == 2:
                cch = chapter(cch)
            chap_dict[k] = cch
    return Manga(
        url             = url,
        title           = ms.select_one(".story-info-right h1").text,
        author          = info("author", lambda x: [i.text for i in x.select("a") if i], []),
        covers          = [ms.select_one(".info-image > img")["src"]],
        alt_titles      = info("alternative", lambda x: [x.text], []),
        status          = info("status", lambda x: {k: v for v, k in enumerate(["ongoing", "completed", "hiatus", "cancelled"])}.get(x.text.lower()), -1),
        genres          = info("genres", lambda x: {i.text: i["href"] for i in x.select("a") if i}, None),
        updated_at      = info("time", lambda x: str(datetime.strptime(x.text[:-3], '%b %d,%Y - %H:%M')), ""),
        created_at      = str(datetime.strptime(rc[-1].select_one("span.chapter-time.text-nowrap")["title"], '%b %d,%Y %H:%M')),
        views           = info("view", lambda x: int(x.text.replace(',', '')), 0),
        description     = ms.select_one(".panel-story-info-description").text,
        chapters        = chap_dict,
    )

def dl_search(title: str, **kwargs: Dict[str, Any]) -> Dict[str, str]:
    title = re.sub(r'[^A-Za-z0-9 ]+', '', title).replace(" ", "_")
    sr = {}
    ms = soup(f"https://manganato.com/search/story/{title}")
    gp = ms.select_one(".group-page")
    if gp:
        for p in range(len(gp.select("a")) - 2):
            for r in soup(f"https://manganato.com/search/story/hello?page={p+1}").select(".a-h.text-nowrap.item-title"):
                sr[r["title"]] = r["href"]
    else:
        for r in ms.select(".a-h.text-nowrap.item-title"):
            sr[r["title"]] = r["href"]
    return sr

def cli_search(title: str, **kwargs: Dict[str, Any]):
    return dl_search(title, **kwargs)

def ch_fn(url: str) -> List[str]:
    return [i["src"] for i in soup(url).select(".container-chapter-reader img")]

def chdls(url: str) -> List[Dict[Union[float, int, None], str]]:
    op = []
    for c in soup(url).select("li.a-h"):
        a = c.select_one("a")
        chdls.append({a["href"].split("-")[-1]: a["href"]})
    return op

def dl(url: str, **kwargs: Dict[str, Any]):
    Downloader(ch_fn, headers={"Referer": "https://readmanganato.com/"}, **kwargs).dl_chdls(chdls(url), soup(url).select_one(".story-info-right h1").text)

def cli_dl(title: str, **kwargs: Dict[str, Any]):
    Downloader(ch_fn, headers={"Referer": "https://readmanganato.com/"}, **kwargs).cli(cli_search, chdls, title)
