from functools import partial
from importlib import import_module
from types import ModuleType
from typing import Any, Callable, Dict, List, Union
from urllib.parse import quote_plus

from bs4 import BeautifulSoup

from ....utils.utils import dt, sanitize_text
from ...base import Ch, Downloader, Manga, soup


class rch_fn:
    def setsu(url: str, base_url: str, manga_id_fn: Callable[[BeautifulSoup], Union[int, float]]):
        data = {"action": "manga_get_chapters", "manga": str(manga_id_fn(soup(url)))}
        return soup(f"{base_url}/wp-admin/admin-ajax.php", method="post", data=data)

class template:
    def __init__(self, prov: ModuleType) -> None:
        self.prov = prov
        ls = ["base_url", "rch_fn", "scanlator"]
        for i in ls:
            setattr(self, i, getattr(prov, i))
        if type(self.rch_fn) == str:
            self.rch_fn = partial(
                getattr(rch_fn, self.rch_fn),
                base_url=self.base_url,
                manga_id_fn=self.prov.manga_id_fn
            )
        self.template = import_module(f".{self.prov.template}", "mangdl.api.providers.templates").template

    def ch_fn(self, url: str) -> List[str]:
        src = getattr(self.prov, "src", "src")
        op = []
        for i in soup(url).select(".page-break img"):
            op.append(sanitize_text(i[src]))
        return op

    def chapter(self, url: str) -> Ch:
        ms = soup(url)
        return Ch(
            url              = url,
            ch               = self.prov.ch_num_fn(ms),
            vol              = None,
            title            = sanitize_text(ms.select_one("ol.breadcrumb .active").text.split("-")[-1]),
            scanlator_groups = [self.scanlator],
            imgs             = self.ch_fn(url),
        )

    def chdls(self, url: str, chs: int=0) -> List[Dict[Union[float, int, None], str]]:
        op = []
        rch = self.rch_fn(url)
        for c in rch.select("li.wp-manga-chapter    a"):
            cch = c["href"]
            if chs == 2:
                cch = self.chapter(cch)
            op.append({self.prov.rch_num_fun(c["href"]): cch})
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

        rch = self.rch_fn(url)
        dates = [sanitize_text(i.text) for i in rch.select(".chapter-release-date")]
        return Manga(
            url             = url,
            covers          = [ms.select_one(".summary_image img")["src"]],
            title           = sanitize_text(ms.select_one("div.post-title h1").text),
            alt_titles      = mst("Alternative"),
            author          = mst("Author(s)", lambda x: x.split(",")),
            artist          = mst("Artist(s)", lambda x: x.split(",")),
            status          = {k: v for v, k in enumerate(["ongoing", "completed", "on hold"])}.get(meta["Status"].lower(), -1),
            genres          = mst("Genre(s)", lambda x: x.split(",")),
            updated_at      = dt(dates[0], r"%B %d, %Y") if dates else "1970-01-01T00:00:00",
            created_at      = dt(dates[-1], r"%B %d, %Y") if dates else "1970-01-01T00:00:00",
            description     = sanitize_text(ms.select_one(".summary__content").text),
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
            url = f"{self.base_url}/page/{num}?s={quote_plus(title)}&post_type=wp-manga"
            ms = soup(url)
            ts = ms.select(cs_manga)
            if not total:
                total = int(sanitize_text(ms.select_one(".c-blog__heading h1").text).split()[0])
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