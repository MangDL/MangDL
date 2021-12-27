from functools import partial
from importlib import import_module
from types import ModuleType
from typing import Any, Callable, Dict, List, Union
from urllib.parse import quote_plus

from bs4 import BeautifulSoup

from ....utils.utils import dt, sanitize_text
from ...base import Ch, Downloader, Manga, soup


class template:
    def __init__(self, prov: ModuleType) -> None:
        self.prov = prov
        ls = ["base_url", "scanlator"]
        for i in ls:
            setattr(self, i, getattr(prov, i))
        self.check_manga = getattr(self.prov, "check_manga", lambda x: True)
        self.template = import_module(f".{self.prov.template}", "mangdl.api.providers.templates").template

    def ch_fn(self, url: str) -> List[str]:
        return [i["src"] for i in soup(url).select("#readerarea p img")]

    def chapter(self, url: str) -> Ch:
        ch = soup(url).select_one("h1.entry-title").text.split()[-1]
        return Ch(
            url              = url,
            ch               = ch,
            vol              = None,
            title            = f"Chapter {ch}",
            scanlator_groups = [self.scanlator],
            imgs             = self.ch_fn(url),
        )

    def chdls(self, url: str, chs: int=0) -> List[Dict[Union[float, int, None], str]]:
        op = []
        for c in soup(url).select("div.eplister ul li"):
            cch = c.select_one("a")["href"]
            if chs == 2:
                cch = self.chapter(cch)
            op.append({c["data-num"]: cch})
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

        rch = self.prov.rch_fn(url)
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
            chapters        = self.chdls(url, chs),
        )

    def manga(self, url: str, chs: int=0) -> Manga:
        ms = soup(url)
        meta = {}
        for m in ms.select(".tsinfo.bixbox .imptdt"):
            i = m.select_one("i")
            meta[m.next_element.strip()] = i.text if i else m.select_one("a").text

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
            chapters        = self.chdls(url, chs),
        )

    def dl_search(self, title: str, **kwargs: Dict[str, Any]) -> Dict[str, str]:
        sr = {}
        def pr(soup: BeautifulSoup):
            for r in soup.select(".listupd .bs .bsx a"):
                if self.check_manga(r):
                    sr[r["title"]] = r["href"]
        ms = soup(f"{self.base_url}/?s={quote_plus(title)}")
        pr(ms)
        pages = ms.select("a.page-numbers")
        if pages:
            for p in range(int(pages[-2].text)-1):
                pr(soup(f"{self.base_url}/page/{p+2}/?s={quote_plus(title)}"))
        return sr

    def cli_search(self, title: str, **kwargs: Dict[str, Any]) -> Dict[str, str]:
        return self.dl_search(title, **kwargs)

    def dl(self, url: str, **kwargs: Dict[str, Any]):
        ms = soup(url)
        Downloader(self.ch_fn, **kwargs).dl_chdls(self.chdls(url), sanitize_text(ms.select_one("div.post-title h1").text))

    def cli_dl(self, title: str, **kwargs: Dict[str, Any]):
        Downloader(self.ch_fn, **kwargs).cli(self.template(self.prov).cli_search, partial(self.chdls), title)