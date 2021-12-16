from typing import Any, Dict, List, Union

from yarl import URL

from ...utils.utils import ddir, dt, dt_ts, squery
from ..base import Ch, Downloader, Manga, Search, req, soup, ddos_guard, urel

def api_series(url: str):
    url = f"https://danke.moe/api/series/{urel(url).parts[3]}/"
    return req.get(url).json()

def chapter(url: str) -> Ch:
    resp = api_series(url)
    url = urel(url)
    slug = url.parts[3]
    ch = int(url.parts[4])
    meta = ddir(resp, f"chapters/{ch}")
    ms = soup(f'https://danke.moe/read/manga/{slug}', ddos_guard)
    bui = f'https://danke.moe/media/manga/{slug}/chapters/{meta["folder"]}/1/'
    return Ch(
        url              = url,
        ch               = ch,
        vol              = meta["volume"],
        title            = meta["title"],
        views            = int(ms.select_one(f'tr[data-chapter="{ch}"] .text-right').text),
        uploaded_at      = dt_ts(ddir(meta, "release_date/1")),
        scanlator_groups = list(resp['groups'].values()),
        user             = "Hachirumi",
        imgs             = [bui + i for i in ddir(meta, "groups/1")],
    )

def manga(url: str, chs: bool=False) -> Manga:
    meta = api_series(url)
    slug = urel(url).parts[3]
    ms = soup(f'https://danke.moe/read/manga/{slug}', ddos_guard)

    chap_dict = {}
    if chs:
        for i in meta["chapters"]:
            chap_dict[i] = chapter(f'https://danke.moe/read/manga/{slug}/{i}')
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
        links           = {"md": rmh("Link").select_one("a")["href"]},
        chapters        = chap_dict,
    )

def dl_search(title: str, **kwargs: Dict[str, Any]) -> Dict[str, str]:
    ms = soup("https://danke.moe/series", ddos_guard)
    all_series = {i.text: i["href"] for i in ms.select("h7.card-title a")}
    sr = {}
    for series, series_url in all_series.items():
        if list(squery(title, [series])):
            sr[series] = series_url
    return sr

def search(s: Search) -> List[Manga]:
    return [manga(i) for i in dl_search(s).values()]

def cli_search(title: str, **kwargs: Dict[str, Any]):
    return dl_search(title, **kwargs)

def ch_fn(url: str) -> List[str]:
    url = urel(url)
    resp = api_series(url)
    meta = ddir(resp, f"chapters/{url.parts[4]}")
    bui = f'https://danke.moe/media/manga/{url.parts[3]}/chapters/{meta["folder"]}/1/'
    return [bui + i for i in ddir(meta, "groups/1")]

def chdls(url: str) -> List[Dict[Union[float, int, None], str]]:
    meta = api_series(url)
    op = []
    for c in meta["chapters"]:
        op.append({c: f"https://danke.moe/read/manga/{urel(url).parts[3]}/{c}/"})
    return op

def dl(url: str, **kwargs: Dict[str, Any]):
    Downloader(ch_fn, **kwargs).dl_chdls(api_series(url)["title"], chdls(url))

def cli_dl(title: str, **kwargs: Dict[str, Any]):
    Downloader(ch_fn, **kwargs).cli(cli_search, chdls, title)
