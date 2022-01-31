from functools import partial
from importlib import import_module
from types import ModuleType
from typing import Any, Callable, Dict, List, Union
from urllib.parse import quote_plus
from ast import literal_eval

from bs4 import BeautifulSoup

from ....utils.utils import dt, sanitize_text
from ...base import Ch, Downloader, Manga, soup, urel

class template:
    def __init__(self, prov: ModuleType) -> None:
        self.prov = prov
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
        if chs:
            for c in self.rch_fn(url).select("li.wp-manga-chapter    a"):
                cch = c["href"]
                if chs == 2:
                    cch = self.chapter(cch)
                op.append({self.rch_num_fn(c["href"]): cch})
        return op

    def manga(self, url: str, chs: int=0) -> Manga:
        url = f'https://reader2.thecatscans.com/series/{(urel(url).parts[2])}'
        ms = soup(url)

        meta = {}
        for i in str(ms.select_one("h1.title + div")).split("<br/> "):
            ss = BeautifulSoup(i, "lxml")
            mn = ss.select_one("b").text
            meta[mn] = sanitize_text(ss.text.replace(f'{mn}: ', ""))

        ch = ms.select(".element .meta_r")
        for i in [0, -1]:
            print(a[i].text[-11:])

        return Manga(
            url             = url,
            covers          = [ms.select_one(".thumbnail img")["src"],],
            title           = ms.select_one("h1.title").text,
            author          = [meta["Author"],],
            artist          = [meta["Artist"],],
            # updated_at      = dates(0),
            # created_at      = dates(-1),
            description     = [meta["Synopsis"],],
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