from functools import partial
from importlib import import_module
from types import ModuleType
from typing import Any, Callable, Dict, List, Union
from urllib.parse import quote_plus
from ast import literal_eval

from bs4 import BeautifulSoup

from ....utils.utils import dt, sanitize_text
from ...base import Ch, Downloader, Manga, soup, urel

class ch_num_fn:
    def breadcrumb(soup):
        return literal_eval(soup.select_one("ol.breadcrumb .active").text.split()[-1])

    def wmcc(soup):
        return literal_eval(".".join(soup.select_one("#wp-manga-current-chap")["value"].split("-")[1:]))

class rch_fn:
    def msa(url: str, base_url: str, **kwargs: Dict[str, Any]):
        url = f"{base_url}/manga/{urel(url).parts[2]}/ajax/chapters/"
        return soup(url, method="post")
    def setsu(url: str, base_url: str, manga_id_fn: Callable[[BeautifulSoup], Union[int, float]], **kwargs: Dict[str, Any]):
        data = {"action": "manga_get_chapters", "manga": str(manga_id_fn(soup(url)))}
        return soup(f"{base_url}/wp-admin/admin-ajax.php", method="post", data=data)

class rch_num_fn:
    def tdo(url):
        return literal_eval(".".join(urel(url).parts[3].split("-")[1:]))

class template:
    def __init__(self, prov: ModuleType) -> None:
        attr = {
            "base_url": None,
            "cover_src": "src",
            "ch_num_fn": ch_num_fn.breadcrumb,
            "rch_fn": soup,
            "rch_num_fn": rch_num_fn.tdo,
            "scanlator": None,
            "search_query_string": "post_type=wp-manga",
            "src": "src",
            "total_cs": ".c-blog__heading h1",
        }
        self.prov = prov
        for k, v in attr.items():
            setattr(self, k, getattr(prov, k, v))
        rfk = ["manga_id_fn"]
        if type(self.rch_fn) == str:
            self.rch_fn = partial(
                getattr(rch_fn, self.rch_fn),
                base_url=self.base_url,
                **{i: getattr(self.prov, i, None) for i in rfk}
            )
        for i in ["ch_num_fn", "rch_num_fn"]:
            gi = getattr(self, i)
            if type(gi) == str:
                setattr(self, i, getattr(globals()[i], getattr(prov, i, gi), gi))

        self.template = import_module(f".{self.prov.template}", "mangdl.api.providers.templates").template

    def ch_fn(self, url: str) -> List[str]:
        op = []
        for i in soup(f"{url}?style=list").select(".page-break img"):
            op.append(sanitize_text(i[self.src]))
        return op

    def chapter(self, url: str) -> Ch:
        ms = soup(url)
        return Ch(
            url              = url,
            ch               = self.ch_num_fn(ms),
            vol              = None,
            title            = sanitize_text(ms.select_one("ol.breadcrumb .active").text.split("-")[-1]),
            scanlator_groups = [self.scanlator],
            imgs             = self.ch_fn(url),
        )

    def chdls(self, url: str, chs: int=0) -> List[Dict[Union[float, int, None], str]]:
        op = []
        for c in self.rch_fn(url).select("li.wp-manga-chapter    a"):
            cch = c["href"]
            if chs == 2:
                cch = self.chapter(cch)
            op.append({self.rch_num_fn(c["href"]): cch})
        return op

    def manga(self, url: str, chs: int=0) -> Manga:
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

        title_fn = getattr(self.prov, "manga_title", None)

        rd = [sanitize_text(i.text) for i in self.rch_fn(url).select(".chapter-release-date")]
        def dates(idx: int):
            op = "1970-01-01T00:00:00"
            if rd:
                rop = rd[idx]
                if rop:
                    op = dt(rop, r"%B %d, %Y")
            return op
        return Manga(
            url             = url,
            covers          = [ms.select_one(".summary_image img")[self.cover_src]],
            title           = title_fn(ms) if title_fn else sanitize_text(ms.select_one("div.post-title h1").text),
            alt_titles      = mst("Alternative"),
            author          = mst("Author(s)", lambda x: x.split(",")),
            artist          = mst("Artist(s)", lambda x: x.split(",")),
            status          = {k: v for v, k in enumerate(["ongoing", "completed", "on hold"])}.get(meta["Status"].lower(), -1),
            genres          = mst("Genre(s)", lambda x: x.split(",")),
            updated_at      = dates(0),
            created_at      = dates(-1),
            description     = sanitize_text(getattr(ms.select_one(".summary__content"), "text", "No description available.")),
            chapters        = self.chdls(url, chs),
        )

    def dl_search(self, title: str, **kwargs: Dict[str, Any]):
        global total
        total = 0
        rpa = getattr(self.prov, "rpa", 12)
        cs_manga = getattr(self.prov, "cs_manga", "div.post-title")
        manga_check = getattr(self.prov, "manga_check", lambda x: True)
        title_fn = getattr(self.prov, "title_fn", lambda x: x.select_one("a").text)
        link_fn = getattr(self.prov, "link_fn", lambda x: x.select_one("a")["href"])
        sr = {}
        def pr(num: int):
            global total
            url = f"{self.base_url}/page/{num}?s={quote_plus(title)}&{self.search_query_string}"
            ms = soup(url)
            ts = ms.select(cs_manga)
            if not total:
                total = int(sanitize_text(ms.select_one(self.total_cs).text).split()[0])
            for r in ts:
                if manga_check(r):
                    sr[title_fn(r)] = link_fn(r)
            return len(ts)
        i = 1
        cp = pr(i)
        while cp // rpa and (rpa * i) < total:
            i += 1
            cp = pr(i)
        return sr

    def cli_search(self, title: str, **kwargs: Dict[str, Any]) -> Dict[str, str]:
        return self.dl_search(title, **kwargs)

    def dl(self, url: str, **kwargs: Dict[str, Any]):
        ms = soup(url)
        Downloader(self.ch_fn, **kwargs).dl_chdls(self.chdls(url), sanitize_text(ms.select_one("div.post-title h1").text))

    def cli_dl(self, title: str, **kwargs: Dict[str, Any]):
        Downloader(self.ch_fn, **kwargs).cli(self.template(self.prov).cli_search, partial(self.chdls), title)