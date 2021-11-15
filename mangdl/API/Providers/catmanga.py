import ast
import difflib
import json
from typing import Any, Callable, Dict, List

import httpx

from ...utils.globals import log
from ...utils.utils import ddir
from ..Base import Ch, Downloader, Manga, req, soup


def manga(url: str) -> Manga:
    """
    Returns a Manga object from the given url.

    Args:
        url (str): url of the manga

    Returns:
        Manga
    """

    meta = req.get(f'https://catmanga.org/api/series/{url.split("/")[-1]}').json()

    def chap_dict():
        n = 1
        op = {}
        for c in meta["chapters"]:
            if ch:=c["number"]:
                k = ch
            else:
                k = -n
                n += 1
            op[k] = Ch(
                url              = "/".join([url, str(ch)]),
                ch               = k,
                vol              = c.get("volume"),
                title            = c["title"],
                scanlator_groups = c["groups"],
            )
        return op

    return Manga(
        url             = url,
        title           = meta["title"],
        author          = meta["authors"],
        covers          = [f'https://images.catmanga.org{i["source"]}' for i in meta["all_covers"]],
        alt_titles      = meta["alt_titles"],
        status          = meta["status"],
        demographics    = meta["genres"][0],
        genres          = meta["genres"][1:],
        description     = meta["description"],
        chapters        = chap_dict(),
    )

def chapter(url: str) -> Ch:
    """
    Return a Ch object from the given url.

    Args:
        url (str): url of the chapter

    Returns:
        Ch
    """
    _meta = ddir(json.loads(soup(url).select_one("#__NEXT_DATA__").text), "props/pageProps")
    def meta(dir: str):
        return ddir(_meta, dir)
    ch = ast.literal_eval(url.split("/")[-1])
    for x in meta("series/chapters"):
        if x["number"] == ch:
            chm = x
            break
    return Ch(
        url              = url,
        ch               = ch,
        vol              = chm.get("volume"),
        title            = chm["title"],
        scanlator_groups = chm["groups"],
        user             = "Black Cat Scanlations",
        imgs             = meta("pages"),
    )

def squery(query: str, possibilities: List[str], cutoff: int=0.6, *, processor: Callable[[Any], Any]=lambda r: r):
    """Custom search query.

    Args:
        query (str): String to search for in the .
        possibilities (List[str]): [description]
        cutoff (int, optional): [description]. Defaults to 0.6.
        processor (Callable[[Any], Any], optional): [description]. Defaults to lambdar:r.

    Yields:
        [type]: [description]
    """


    sequence_matcher = difflib.SequenceMatcher()
    sequence_matcher.set_seq2(query)

    for search_value in possibilities:
        sequence_matcher.set_seq1(processor(search_value))
        if (query.lower() in processor(search_value).lower()):
            yield (None, search_value)
            continue
        if (sequence_matcher.real_quick_ratio() >= cutoff and sequence_matcher.quick_ratio(
        ) >= cutoff and sequence_matcher.ratio() >= cutoff):
            yield (sequence_matcher.ratio(), search_value)

def search(query: str):
    """Can be used for searching manga when using this project as a module.

    Args:
        s (Search): Search dataclass, search parameters for searching.

    Returns:
        List[Manga]: Search results.
    """
    all_series = httpx.get("https://catmanga.org/api/series/allSeries").json()
    sr = []

    for series in all_series:
        def meta(m: str):
            return ddir(series, m)
        if list(squery(query, [meta("title"), *meta("alt_titles")], 0.39)):
            sr.append(
                Manga(
                    url = f'https://catmanga.org/series/{meta("series_id")}',
                    title = meta("title"),
                    author = meta("authors"),
                    covers=[meta("cover_art/source")],
                    alt_titles=meta("alt_titles"),
                    demographics=meta("genres")[0],
                    genres=meta("genres")[1:],
                    description=meta("description"),
                )
            )

    return sr

def dl_search(title: str, **kwargs: Dict[str, Any]):
    """Used for downloading when imported.

    Args:
        s (Search): [description]

    Returns:
        Dict[str, str]: [description]
    """

    all_series = httpx.get("https://catmanga.org/api/series/allSeries").json()

    sr = {}

    for series in all_series:
        if list(squery(title, [series["title"], *series["alt_titles"]], 0.39)):
            sr[series["title"]] = f'https://catmanga.org/series/{series["series_id"]}'
    return sr

def cli_search(title: str, **kwargs: Dict[str, Any]):
    """Format click arguments and options to their respective types,
    then pass that to `dl_search` for it to return the search results.

    Args:
        title (str): Title of the manga to search for.

    Returns:
        Dict[str, str]: Search results
    """

    log.info("Ignoring all keword arguments.", "cli_search")
    return dl_search(title, **kwargs)

def dl(url: str, **kwargs: Dict[str, Any]):
    """Used for downloading when using the project as a module.

    Args:
        url (str): URL of the manga to download.
    """

    meta = ddir(json.loads(soup(url).select_one("#__NEXT_DATA__").text), "props/pageProps/series")
    def ch_fn(url: str):
        return ddir(json.loads(soup(url).select_one("#__NEXT_DATA__").text), "props/pageProps/pages")
    chdls = []
    for c in meta["chapter"]:
        num = c["number"]
        chdls.append({num: f"{url}/{num}"})
    Downloader(ch_fn, **kwargs).dl_chdls(meta["title"], chdls)

def cli_dl(title: str, **kwargs: Dict[str, Any]):
    """Used for downloading when using cli.

    Args:
        title (str): Title of the manga to download.
    """

    sr = cli_search(title)
    def ch_fn(url: str):
        return ddir(json.loads(soup(url).select_one("#__NEXT_DATA__").text), "props/pageProps/pages")
    def chs_fn(choice: str):
        op = []
        url = sr[choice]
        for c in ddir(json.loads(soup(url).select_one("#__NEXT_DATA__").text), "props/pageProps/series/chapters"):
            num = c["number"]
            op.append({num: f"{url}/{num}"})
        return op
    Downloader(ch_fn, **kwargs).cli(sr, chs_fn)
