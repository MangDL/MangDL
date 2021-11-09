import difflib
from typing import Any, Callable, Dict, List
import httpx

import ast

from ..Base import Ch, Downloader, Manga, Search, soup, req
from ...utils.utils import ddir

import json

# def manga(url: str) -> Manga:
#     """
#     Returns a Manga object from the given url.

#     Args:
#         url (str): url of the manga

#     Returns:
#         Manga
#     """

#     _meta = ddir(json.loads(soup(url).select_one("#__NEXT_DATA__").text), "props/pageProps/series")
#     def meta(m: str):
#         return ddir(_meta, m)

#     def chap_dict():
#         n = 1
#         op = {}
#         for c in meta("chapters"):
#             if ch:=c["number"]:
#                 k = ch
#             else:
#                 k = -n
#                 n += 1
#             op[k] = Ch(
#                 url              = "/".join([url, str(ch)]),
#                 ch               = k,
#                 vol              = c.get("volume"),
#                 title            = c["title"],
#                 scanlator_groups = c["groups"],
#             )
#         return op

#     return Manga(
#         url             = url,
#         title           = meta("title"),
#         author          = meta("authors"),
#         covers          = [meta("cover_art/source")],
#         alt_titles      = meta("alt_titles"),
#         status          = meta("status"),
#         demographics    = meta("genres")[0],
#         genres          = meta("genres")[1:],
#         description     = meta("description"),
#         chapters        = chap_dict(),
#     )

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

def squery(query: str, possibilities: List[str], cutoff: int=0.6, *, processor: Callable[[Any], Any]=lambda r: r):

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
    all_series = httpx.get("https://catmanga.org/api/series/allSeries").json()

    sr = {}

    for series in all_series:
        if list(squery(title, [series["title"], *series["alt_titles"]], 0.39)):
            sr[series["title"]] = f'https://catmanga.org/series/{series["series_id"]}'
    return sr

def cli_search(title: str, **kwargs: Dict[str, Any]):
    log.info("Ignoring all keword arguments.", "cli_search")
    return dl_search(title, **kwargs)
