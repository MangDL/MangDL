import ast
import time
from typing import Any, Dict, List

import httpx

from ...utils import globals
from ...utils.globals import log
from ...utils.settings import stg
from ...utils.utils import ddir, de, dnrp, parse_list
from ..Base import Ch, Downloader, Manga, Search, Vls, req

if not globals.log:
    from ...utils.log import logger
    log = logger(2)

def ra(resp: httpx.Response) -> int:
    """Return the current time subracted to retry after header from the given
    response object.

    Args:
        resp (httpx.Response): Response object to get the retry after header from.

    Returns:
        int: current time subracted to retry after header.
    """
    op = int(resp.headers["X-RateLimit-Retry-After"]) - int(time.time()) + 1
    return op

def value(d: Dict[Any, Any]) -> Any:
    """Returns the first value of the first key from a dictionary

    Args:
        d (dict[Any, Any]): Dictionary to get the first value from.

    Returns:
        Any: First value of the given dictionary.
    """
    return list(d.values())[0]

def paginate(url: str, limit: int = 100, params: Dict[Any, Any] = {}) -> List[Dict[str, Any]]:
    """Paginate results from an API endpoint with limited results per calls.

    Args:
        log (Callable[[str, str, str], None]): logger
        url (str): url of the endpoint
        limit (int, optional): items per page. Defaults to 100.
        params (dict[Any, Any], optional): parameters for the request. Defaults to {}.

    Returns:
        list[dict[str, Any]]: paginated results
    """

    log.info(f'Paginating {url} with the following parameters excluding "limit" and "offset": {params}', 'paginator')
    def get_page(offset: int=0):
        log.debug(f'Paginating results from {offset} to {offset+limit}', 'paginator')
        return req.get(url, ra, params={k: d[k] for d in [{"limit": limit, "offset": offset}, params] for k in d}).json()

    ls = []
    offset = 0
    x = get_page(offset)
    ls.append(x)


    while x["total"] - (offset + 100) > 0:
        offset += 100
        ls.append(get_page(offset))
    log.debug(f'Paginating finished. {len(ls)} page{"s are" if len(ls) > 1 else " is"} returned.', 'paginator')
    return ls


def manga(url: str) -> Manga:
    """Returns a Manga object from the given url.

    Args:
        url (str): url of the manga

    Returns:
        Manga
    """

    op_links = {
        "al": "https://anilist.co/manga/{}",
        "ap": "https://www.anime-planet.com/manga/{}",
        "bw": "https://bookwalker.jp/{}",
        "mu": "https://www.mangaupdates.com/series.html?id={}",
        "nu": "https://www.novelupdates.com/series/{}",
        "kt": "https://kitsu.io/api/edge/manga?filter[slug]={}",
        "mal": "https://myanimelist.net/manga/{}"
    }

    url_parts = url.split('/')
    if len(url_parts) == 5:
        manga_id = url_parts[-1]
    else:
        manga_id = url
    resp_obj = req.get(f"https://api.mangadex.org/manga/{manga_id}?includes[]=author&includes[]=artist&includes[]=cover_art", ra).json()
    relps = ddir(resp_obj, "data/relationships")

    def attr(dir: str):
        return ddir(resp_obj, f"data/attributes/{dir}")

    def relp(x: str):
        return [i for i in relps if i["type"] == x][0]

    links = attr("links")

    def chap_dict():
        n = 1
        op = {}
        for d in paginate(f"https://api.mangadex.org/manga/{manga_id}/feed", 500, {"translatedLanguage[]": "en", "order[chapter]": "desc"}):
            for r in d["data"]:
                ch = ddir(r, "attributes/chapter")
                if ch:
                    k = ast.literal_eval(ch)
                else:
                    k = -n
                    n += 1
                vol = ddir(r, "attributes/volume")
                op[k] = Ch(
                    url         = f"https://mangadex.org/chapter/{ddir(r, 'id')}",
                    ch          = k,
                    vol         = ast.literal_eval(vol) if vol else vol,
                    title       = ddir(r, "attributes/title"),
                    uploaded_at = ddir(r, "attributes/publishAt"),
                )
        return op

    return Manga(
        url             = url,
        covers          = [f"https://uploads.mangadex.org/covers/{manga_id}/{ddir(c, 'attributes/fileName')}" for i in paginate(f"https://api.mangadex.org/cover?manga[]={manga_id}") for c in i["data"]],
        title           = value(attr("title")),
        alt_titles      = [value(i) for i in attr("altTitles")],
        author          = ddir(relp("author"), "attributes/name"),
        status          = {k: v for v, k in enumerate(["ongoing", "completed", "hiatus", "cancelled"])}.get(attr("status"), -1),
        demographics    = attr("publicationDemographic"),
        content_rating  = attr("contentRating"),
        genres          = {value(ddir(i, "attributes/name")): i["id"] for i in attr("tags") if ddir(i, "attributes/group") == "genre"},
        updated_at      = attr("updatedAt"),
        created_at      = attr("createdAt"),
        description     = attr("description/en"),
        links           = {k: op_links[k].format(v) if k in op_links else v for k, v in links.items()} if links else {},
        chapters        = chap_dict(),
    )


def chapter(url: str) -> Ch:
    """Return a Ch object from the given url.

    Args:
        url (str): url of the chapter

    Returns:
        Ch
    """

    id = url.split("chapter/")[1]
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

def dl_search(s: Search) -> Dict[str, str]:
    """Used for downloading when imported.

    Args:
        s (Search): [description]

    Returns:
        Dict[str, str]: [description]
    """

    params = []
    sr = {}
    ad = stg(f"mangadex/search", f"{dnrp(__file__, 3)}/utils/config.yaml")
    for k in s.__dataclass_fields__:
        v = getattr(s, k)
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

def search(s: Search) -> List[Manga]:
    """Can be used for searching manga when using this project as a module.

    Args:
        s (Search): Search dataclass, search parameters for searching.

    Returns:
        List[Manga]: Search results.
    """
    return [manga(i) for i in dl_search(s).values()]

def cli_search(title: str, **kwargs: Dict[str, Any]) -> Dict[str, str]:
    """Format click arguments and options to their respective types,
    then pass that to `dl_search` for it to return the search results.

    Args:
        title (str): Title of the manga to search for.

    Returns:
        Dict[str, str]: Search results
    """
    params = {}
    tags = {ddir(t, "attributes/name/en").lower(): t["id"] for t in req.get("https://api.mangadex.org/manga/tag", ra).json()["data"]}
    vls = {"tags": [*tags.keys()]}
    for k, v in stg(f"mangadex/cli_search", f"{dnrp(__file__, 3)}/utils/config.yaml").items():
        op = []
        v = de(v, [])
        strings = parse_list(kwargs[k])
        v, lsn, w = [*v, *[None for _ in range(3 - len(v))]]
        if strings:
            for string in strings:
                if v:
                    if string in (v if type(v) is list else vls[v]):
                        op.append(v[string] if type(v) == dict else string)
                    else:
                        log.warning(f'"{string}" not in {lsn}.{f" {w}" if w else ""}', k)
                else:
                    op.append(string)
            params[k] = op
        else:
            log.debug(f'"{k}" option is empty.', k)
    if kwargs["order"]:
        o, s = kwargs["order"].split(":")
        if o not in ['title', 'year', 'createdAt', 'updatedAt', 'latestUploadedChapter', 'followedCount', 'relevance']:
            log.warning(f'"{o}" not in list of order. (title | year | createdAt | updatedAt | latestUploadedChapter | followedCount | relevance):(asc | desc)', "order")
            o = None
        if s not in ['asc', 'desc']:
            log.warning(f'"{s}" not in list of order. (title | year | createdAt | updatedAt | latestUploadedChapter | followedCount | relevance):(asc | desc)', "order")
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
        if im in ["AND", "OR"]:
            if it:
                params["includemode"] = im
            else:
                log.warning('"includemode" option has an argument passed to it despite the option "includetags" being empty, will not be used to filter search results.', "includemode")
        else:
            log.warning(f'"{im}" not in list of includedTagsMode. (AND | OR)', "includemode")
            im = None
    elif it:
        log.debug('"includemode" option is empty, dafaults to "AND".', "includetags")
    em = kwargs["excludemode"]
    et = not not kwargs["excludetags"]
    if em:
        em = em.upper()
        if em in ["AND", "OR"]:
            if et:
                params["excludemode"] = em
            else:
                log.warning('"excludemode" option has an argument passed to it despite the option "excludetags" being empty, will not be used to filter search results.', "excludemode")
        else:
            log.warning(f'"{em}" not in list of excludedTagsMode. (AND | OR)', "excludemode")
            em = None
    elif et:
        log.debug('"excludemode" option is empty, defaults to "OR".', "excludetags")

    return dl_search(Search(title, **params))

def dl(url: str, **kwargs: Dict[str, Any]):
    """Used for downloading when using the project as a module.

    Args:
        url (str): URL of the manga to download.
    """
    def ch_fn(id: str):
        resp_obj = req.get(f"https://api.mangadex.org/chapter/{id}", ra).json()
        hash = ddir(resp_obj, 'data/attributes/hash')
        bu = req.get(f"https://api.mangadex.org/at-home/server/{ddir(resp_obj, 'data/id')}", ra).json()["baseUrl"]
        return [f"{bu}/data/{hash}/{i}" for i in ddir(resp_obj, "data/attributes/data")]
    url_parts = url.split('/')
    if len(url_parts) == 5:
        manga_id = url_parts[-1]
    else:
        manga_id = url
    chdls = []
    for i in paginate(f"https://api.mangadex.org/manga/{manga_id}/feed", 500, {"translatedLanguage[]": "en", "order[chapter]": "desc"}):
        for d in i["data"]:
            chdls.append({ddir(d, "attributes/chapter"): d["id"]})
    Downloader(ch_fn, ra, **kwargs).dl_chdls(ddir(*req.get(f"https://api.mangadex.org/manga/{manga_id}").json(), "data/attributes/title").values()[0], chdls)

def cli_dl(title: str, **kwargs: Dict[str, Any]):
    """Used for downloading when using cli.

    Args:
        title (str): Title of the manga to download.
    """
    sr = cli_search(title, **kwargs)
    def ch_fn(id: str):
        resp_obj = req.get(f"https://api.mangadex.org/chapter/{id}", ra).json()
        hash = ddir(resp_obj, 'data/attributes/hash')
        bu = req.get(f"https://api.mangadex.org/at-home/server/{ddir(resp_obj, 'data/id')}", ra).json()["baseUrl"]
        return [f"{bu}/data/{hash}/{i}" for i in ddir(resp_obj, "data/attributes/data")]
    def chs_fn(choice: str):
        url = sr[choice]
        url_parts = url.split('/')
        if len(url_parts) == 5:
            manga_id = url_parts[-1]
        else:
            manga_id = url
        op = []
        for i in paginate(f"https://api.mangadex.org/manga/{manga_id}/feed", 500, {"translatedLanguage[]": "en", "order[chapter]": "desc"}):
            for d in i["data"]:
                op.append({ddir(d, "attributes/chapter"): d["id"]})
        return op
    Downloader(ch_fn, ra, **kwargs).cli(sr, chs_fn)
