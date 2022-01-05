import ast
import time
from typing import Any, Dict, List, Union

import httpx
from yarl import URL

from ...utils.settings import stg
from ...utils.utils import ddir, de, dnrp, parse_list
from ..base import Ch, Downloader, Manga, Vls, req

op_links = {
    "al": "https://anilist.co/manga/{}",
    "ap": "https://www.anime-planet.com/manga/{}",
    "bw": "https://bookwalker.jp/{}",
    "mu": "https://www.mangaupdates.com/series.html?id={}",
    "nu": "https://www.novelupdates.com/series/{}",
    "kt": "https://kitsu.io/api/edge/manga?filter[slug]={}",
    "mal": "https://myanimelist.net/manga/{}"
}

def ra(resp: httpx.Response) -> int:
    op = resp.headers.get("X-RateLimit-Retry-After")
    if op:
        op = int(op) - int(time.time()) + 1
    else:
        op = int(resp.headers['retry-after'])
    return op

def value(d: Dict[Any, Any]) -> Any:
    return list(d.values())[0]

def paginate(url: str, limit: int = 100, params: Dict[Any, Any] = {}) -> List[Dict[str, Any]]:
    def get_page(offset: int=0):
        return req.get(url, ra, params={k: d[k] for d in [{"limit": limit, "offset": offset}, params] for k in d}).json()

    ls = []
    offset = 0
    x = get_page(offset)
    ls.append(x)

    while x["total"] - (offset + 100) > 0:
        offset += 100
        ls.append(get_page(offset))
    return ls

def url_id(url: str) -> str:
    url = URL(url)
    if url.is_absolute():
        url = url.relative()
    return url.parts[2]

def chapter(url: str) -> Ch:
    id = url_id(url)
    resp_obj = req.get(f"https://api.mangadex.org/chapter/{id}", params={"includes[]": "scanlation_group"}).json()

    def attr(dir: str):
        return ddir(resp_obj, f"data/attributes/{dir}")

    bu = req.get(f"https://api.mangadex.org/at-home/server/{ddir(resp_obj, 'data/id')}", ra).json()["baseUrl"]

    ch = attr("chapter")
    vol = attr("volume")
    return Ch(
        url         = url,
        ch          = ast.literal_eval(ch) if ch else ch,
        vol         = ast.literal_eval(vol) if vol else vol,
        title       = attr("title"),
        uploaded_at = attr("publishAt"),
        imgs        = [f"{bu}/data/{attr('hash')}/{i}" for i in attr("data")],
    )

def manga(url: str, chs: int=0) -> Manga:
    id = url_id(url)
    resp_obj = req.get(f"https://api.mangadex.org/manga/{id}?includes[]=author&includes[]=artist&includes[]=cover_art", ra).json()
    relps = ddir(resp_obj, "data/relationships")

    def attr(dir: str) -> Any:
        return ddir(resp_obj, f"data/attributes/{dir}")

    def relp(x: str) -> str:
        return [i for i in relps if i["type"] == x][0]

    links = attr("links")

    chap_dict = {}
    if chs:
        n = 1
        for d in paginate(f"https://api.mangadex.org/manga/{id}/feed", 500, {"translatedLanguage[]": "en", "order[chapter]": "desc"}):
            for r in d["data"]:
                ch = ddir(r, "attributes/chapter")
                if ch:
                    k = ast.literal_eval(ch)
                else:
                    k = -n
                    n += 1
                cch = f"https://mangadex.org/chapter/{ddir(r, 'id')}"
                if chs == 2:
                    cch = chapter(cch)
                chap_dict[k] = cch

    return Manga(
        url             = url,
        covers          = [f"https://uploads.mangadex.org/covers/{id}/{ddir(c, 'attributes/fileName')}" for i in paginate(f"https://api.mangadex.org/cover?manga[]={id}") for c in i["data"]],
        title           = value(attr("title")),
        alt_titles      = [value(i) for i in attr("altTitles")],
        author          = [ddir(relp("author"), "attributes/name")],
        artist          = [ddir(relp("artist"), "attributes/name")],
        status          = {k: v for v, k in enumerate(["ongoing", "completed", "hiatus", "cancelled"])}.get(attr("status"), -1),
        demographics    = attr("publicationDemographic"),
        content_rating  = attr("contentRating"),
        genres          = {value(ddir(i, "attributes/name")): i["id"] for i in attr("tags") if ddir(i, "attributes/group") == "genre"},
        updated_at      = attr("updatedAt"),
        created_at      = attr("createdAt"),
        description     = attr("description/en"),
        links           = {k: op_links[k].format(v) if k in op_links else v for k, v in links.items()} if links else {},
        chapters        = chap_dict,
    )

def dl_search(title: str, **kwargs: Dict[str, Any]) -> Dict[str, str]:
    local = {"title": title, **kwargs}
    params = []
    sr = {}
    ad = stg(f"mangadex/search", f"{dnrp(__file__, 3)}/utils/config.yaml")
    for k in local:
        v = local.get(k)
        if type(v) is str:
            params.append(f"{k}={v}")
        elif type(v) is list:
            for vv in v:
                params.append(f"{ad[k]}[]={vv}")
        elif type(v) is dict:
            for vk, vv in v.items():
                params.append(f"{ad[k]}[{vk}]={vv}")
        elif type(v) is Vls:
            for vk in v.ls:
                vv = v.vdict.get(vk, None)
                if vv:
                     params.append(f"{ad[k]}[]={vv}")
    for page in paginate(f'https://api.mangadex.org/manga?{"&".join(params)}'):
        for comic in page["data"]:
            sr[value(ddir(comic, "attributes/title"))] = f'https://mangadex.org/title/{comic["id"]}'
    return sr

def cli_search(title: str, **kwargs: Dict[str, Any]) -> Dict[str, str]:
    params = {}
    tags = {ddir(t, "attributes/name/en").lower(): t["id"] for t in req.get("https://api.mangadex.org/manga/tag", ra).json()["data"]}
    vls = {"tags": [*tags.keys()]}
    for k, v in stg(f"mangadex/cli_search", f"{dnrp(__file__, 3)}/utils/config.yaml").items():
        op = []
        v = de(v, [])
        strings = parse_list(kwargs[k])
        if strings:
            for string in strings:
                if v and string in (v if type(v) is list else vls[v]):
                        op.append(v[string] if type(v) == dict else string)
                else:
                    op.append(string)
            params[k] = op
    if kwargs["order"]:
        o, s = kwargs["order"].split(":")
        if o not in ['title', 'year', 'createdAt', 'updatedAt', 'latestUploadedChapter', 'followedCount', 'relevance']:
            o = None
        if s not in ['asc', 'desc']:
            s = None
        if o and s:
            params["order"] = Vls(o, s)
    year = kwargs["year"]
    if year:
        params.append(f'year={year}')
    tags = {ddir(t, "attributes/name/en").lower(): t["id"] for t in req.get("https://api.mangadex.org/manga/tag", ra).json()["data"]}
    im = kwargs["includemode"]
    it = not not kwargs["includetags"]
    if im:
        im = im.upper()
        if im in ["AND", "OR"] and it:
            params["includemode"] = im
        else:
            im = None
    em = kwargs["excludemode"]
    et = not not kwargs["excludetags"]
    if em:
        em = em.upper()
        if em in ["AND", "OR"] and et:
            params["excludemode"] = em
        else:
            em = None

    return dl_search(title, **params)

def ch_fn(url: str) -> List[str]:
    resp_obj = req.get(f"https://api.mangadex.org/chapter/{id}", ra).json()
    hash = ddir(resp_obj, 'data/attributes/hash')
    bu = req.get(f"https://api.mangadex.org/at-home/server/{ddir(resp_obj, 'data/id')}", ra).json()["baseUrl"]
    return [f"{bu}/data/{hash}/{i}" for i in ddir(resp_obj, "data/attributes/data")]

def chdls(url: str) -> List[Dict[Union[float, int, None], str]]:
    id = url_id(url)
    op = []
    for i in paginate(f"https://api.mangadex.org/manga/{id}/feed", 500, {"translatedLanguage[]": "en", "order[chapter]": "desc"}):
        for d in i["data"]:
            op.append({ddir(d, "attributes/chapter"): d["id"]})
    return op

def dl(url: str, **kwargs: Dict[str, Any]):
    id = url_id(url)
    Downloader(ch_fn, ra, **kwargs).dl_chdls(chdls(url), *ddir(req.get(f"https://api.mangadex.org/manga/{id}").json(), "data/attributes/title").values())

def cli_dl(title: str, **kwargs: Dict[str, Any]):
    Downloader(ch_fn, **kwargs).cli(cli_search, chdls, title)
