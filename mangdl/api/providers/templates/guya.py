from functools import partial
from types import ModuleType
from typing import Any, Dict, List, Union

from yarl import URL

from ....utils.utils import ddir, dt, dt_ts, squery
from ...base import (Ch, Downloader, Manga, ddos_cookies, ddos_guard, req,
                     soup, urel)


class template:
    def __init__(self, prov: ModuleType) -> None:
        self.prov = prov
        ls = ["base_url", "scanlator"]
        for i in ls:
            setattr(self, i, getattr(prov, i))
        self.links_fn = getattr(self.prov, "links_fn", lambda x: {})

    def api_series(self, url: str):
        url = f"{self.base_url}/api/series/{urel(url).parts[3]}/"
        return req.get(url).json()

    def ch_fn(self, url: str) -> List[str]:
        url = urel(url)
        resp = self.api_series(url)
        meta = ddir(resp, f"chapters/{url.parts[4]}")
        group, imgs = list(ddir(meta, "groups").items())[0]
        bui = f'{self.base_url}/media/manga/{url.parts[3]}/chapters/{meta["folder"]}/{group}/'
        return [bui + i for i in imgs]

    def chapter(self, url: str) -> Ch:
        resp = self.api_series(url)
        url = urel(url)
        slug = url.parts[3]
        ch = int(url.parts[4])
        meta = ddir(resp, f"chapters/{ch}")
        ms = soup(f'{self.base_url}/read/manga/{slug}', ddos_guard)
        return Ch(
            url              = url,
            ch               = ch,
            vol              = meta["volume"],
            title            = meta["title"],
            views            = int(ms.select_one(f'tr[data-chapter="{ch}"] .text-right').text),
            uploaded_at      = dt_ts(list(ddir(meta, "release_date").values())[0]),
            scanlator_groups = list(resp['groups'].values()),
            user             = [self.scanlator],
            imgs             = self.ch_fn(url),
        )

    def chdls(self, url: str, chs: int=0) -> List[Dict[Union[float, int, None], str]]:
        meta = self.api_series(url)
        op = []
        for c in meta["chapters"]:
            cch = f"{self.base_url}/read/manga/{urel(url).parts[3]}/{c}/"
            if chs == 2:
                cch = self.chapter(cch)
            op.append({c: cch})
        return op

    def manga(self, url: str, chs: int=0) -> Manga:
        meta = self.api_series(url)
        slug = urel(url).parts[3]
        ms = soup(f'{self.base_url}/read/manga/{slug}', ddos_guard)

        mls = [i.text for i in ms.select('.col-lg-8 table.table-borderless th')]
        def rmh(meta: str):
            idx = mls.index(meta) + 1
            cs = f'.col-lg-8 table.table-borderless tr:nth-child({idx}) td'
            return ms.select_one(cs)
        def mh(meta: str):
            return rmh(meta).text

        return Manga(
            url             = str(URL.build(scheme="https", host="danke.moe", path=urel(url).path)),
            covers          = [meta["cover"]],
            title           = meta["title"],
            author          = [meta["author"]],
            created_at      = dt(mh("Last Updated").split(" - ")[1], "%Y-%m-%d"),
            views           = int(mh("Views")),
            description     = ms.select_one("div.col-md-7 > article > p").text,
            links           = self.links_fn(rmh),
            chapters        = self.chdls(url, chs),
        )

    def dl_search(self, title: str, **kwargs: Dict[str, Any]) -> Dict[str, str]:
        ms = soup(f"{self.base_url}/series", ddos_guard)
        all_series = {i.text: i["href"] for i in ms.select("h7.card-title a")}
        sr = {}
        for series, series_url in all_series.items():
            if list(squery(title, [series])):
                sr[series] = self.base_url + series_url
        return sr

    def cli_search(self, title: str, **kwargs: Dict[str, Any]):
        return self.dl_search(title, **kwargs)

    def cli_dl(self, title: str, **kwargs: Dict[str, Any]):
        Downloader(self.ch_fn, cookies=ddos_cookies, **kwargs).cli(self.cli_search, partial(self.chdls), title)