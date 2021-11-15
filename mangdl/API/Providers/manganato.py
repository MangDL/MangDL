import ast
import re
from datetime import datetime
from typing import Any, Callable, Dict

from ...utils.globals import log
from ..Base import Ch, Downloader, Manga, Search, soup


def manga(url: str) -> Manga:
    log.debug(f"Converting {url} to Manga dataclass.", "manga")
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
    def chap_dict():
        n = 1
        op = {}
        for c in rc:
            a = c.select_one("a")
            ch = a["href"].split("-")[-1]
            if ch:
                k = ast.literal_eval(ch)
            else:
                k = -n
                n += 1
            op[k] = Ch(
                url             = a["href"],
                ch              = k,
                vol             = None,
                title           = a.text,
                views           = int(c.select_one("span.chapter-view.text-nowrap").text.replace(",", "")),
                uploaded_at     = str(datetime.strptime(c.select_one("span.chapter-time.text-nowrap")["title"], '%b %d,%Y %H:%M')),
            )
        return op
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
        chapters        = chap_dict(),
    )

def chapter(url: str) -> Ch:
    log.debug(f"Converting {url} to Ch dataclass.", "chapter")
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

def search(s: Search):
    log.info("Ignoring all keword arguments at the moment. Will add advanced searching later.", "search")
    title = re.sub(r'[^A-Za-z0-9 ]+', '', s.title).replace(" ", "_")
    sr = {}
    ms = soup(f"https://manganato.com/search/story/{title}")
    gp = ms.select_one(".group-page")
    if gp:
        log.debug("Multiple pages found. Starting to paginate.", "paginator")
        for p in range(len(gp.select("a")) - 2):
            log.debug(f"Paginating page {p+1}.", "paginator")
            for r in soup(f"https://manganato.com/search/story/hello?page={p+1}").select(".a-h.text-nowrap.item-title"):
                sr[r["title"]] = r["href"]
    else:
        log.debug("Only one page found.", "search")
        for r in ms.select(".a-h.text-nowrap.item-title"):
            sr[r["title"]] = r["href"]
    return sr

def cli_search(title: str, **kwargs: Dict[str, Any]):
    log.debug('No processing to do with the arguments, will be immediately passed to the function "search".', "cli search")
    return search(Search(title, **kwargs))

def dl(url: str, **kwargs: Dict[str, Any]):
    ms = soup(url)
    def ch_fn(url: str):
        return [i["src"] for i in soup(url).select(".container-chapter-reader img")]
    chdls = []
    for c in ms.select("li.a-h"):
        a = c.select_one("a")
        chdls.append({a["href"].split("-")[-1]: a["href"]})
    Downloader(ch_fn, headers={"Referer": "https://readmanganato.com/"}, **kwargs).cli(ms.select_one(".story-info-right h1").text, chdls)

def cli_dl(title: str, **kwargs: Dict[str, Any]):
    sr = cli_search(title)
    def ch_fn(url: str):
        return [i["src"] for i in soup(url).select(".container-chapter-reader img")]
    def chs_fn(choice: str):
        op = []
        for c in soup(sr[choice]).select("li.a-h"):
            a = c.select_one("a")
            op.append({a["href"].split("-")[-1]: a["href"]})
        return op
    Downloader(ch_fn, headers={"Referer": "https://readmanganato.com/"}, **kwargs).cli(sr, chs_fn)
