import importlib
import os
import re
import shutil
import sys
import time
from dataclasses import dataclass, field
from functools import lru_cache, partial
from multiprocessing.pool import ThreadPool
from typing import Any, Callable, Dict, List, Union
import ast

import click
import httpx
import patoolib
from bs4 import BeautifulSoup
from tabulate import tabulate
from tqdm import tqdm
from yachalk import chalk

from ..utils import style
from ..utils.globals import log
from ..utils.settings import stg

session = httpx.Client()

def base(url: str, connector: str, info: str):
    return getattr(importlib.import_module(f'mangdl.API.Providers.{connector}'), info)(url)

def _req(url: str, ra: Callable[[httpx.Response], int]=None, method: str = "get", session: httpx.Client = session, *args: List[Any], **kwargs: Dict[str, Any]):
    resp = getattr(session, method)(url, *args, **kwargs)
    if resp.status_code == 429:
        if ra:
            time.sleep(ra(resp))
            return _req(url, ra, method, session, *args, **kwargs)
    return resp

class req:
    pass

for i in ["get", "options", "head", "post", "put", "patch", "delete"]:
    setattr(req, i, partial(_req, method=i))

def headers(d: Dict[Any, Any] = {}) -> Dict[Any, Any]:
    return {k: d[k] for k in d for d in [stg("Network/headers"), d]}

@lru_cache()
def soup(url: str) -> BeautifulSoup:
    """Returns a soup.
    (petition to rename this function to sauce!)

    Args:
        url (str): URL to get the soup from.

    Returns:
        BeautifulSoup: the soup
    """
    return BeautifulSoup(req.get(url).text, "lxml")

@dataclass
class Vls:
    vdict   : Dict[str, Any]
    ls      : List[str]


@dataclass
class SearchResults:
    title   : str
    link    : str

@dataclass
class Search:
    title           : str
    lang            : List[str]                             = field(default_factory=list)
    excludelang     : List[str]                             = field(default_factory=list)
    demo            : List[str]                             = field(default_factory=list)
    contentrating   : List[str]                             = field(default_factory=list)
    status          : List[str]                             = field(default_factory=list)
    order           : str                                   = field(default_factory=dict)
    authors         : List[str]                             = field(default_factory=list)
    artists         : List[str]                             = field(default_factory=list)
    year            : int                                   = None
    includetags     : List[str]                             = field(default_factory=list)
    includemode     : str                                   = None
    excludetags     : List[str]                             = field(default_factory=list)
    excludemode     : str                                   = None
    range           : Callable[[Union[int, float]], bool]   = lambda *args, **kwargs: True
    cover           : bool                                  = False
    directory       : str                                   = None
    overwrite       : bool                                  = False
    retry           : int                                   = 3
    retryprompt     : bool                                  = False
    threads         : int                                   = 5
    verbosity       : int                                   = 4
    saveconfig      : str                                   = None
    loadconfig      : str                                   = None
    overridelc      : bool                                  = False


@dataclass
class CliSearch:
    title           : str
    lang            : str
    excludelang     : str
    demo            : str
    contentrating   : str
    status          : str
    order           : str
    authors         : str
    artists         : str
    year            : int
    includetags     : str
    includemode     : str
    excludetags     : str
    excludemode     : str
    range           : str
    cover           : bool
    directory       : str
    overwrite       : bool
    retry           : int
    retryprompt     : bool
    threads         : int
    verbosity       : int
    saveconfig      : str
    loadconfig      : str
    overridelc      : bool


@dataclass
class Ch:
    """Use the template below:
    Ch(
        url             =
        ch              =
        vol             =
        title           =
        views           =
        uploaded_at     =
        scanlator_group =
        user            =
        imgs            =
    )
    """
    url             : str
    ch              : Union[int, float, None]
    vol             : Union[int, float, None]
    title           : str
    views           : int                       = 0
    uploaded_at     : str                       = None
    scanlator_group : List[str]                 = field(default_factory=list)
    user            : str                       = None
    imgs            : List[str]                 = field(default_factory=list)


@dataclass
class Manga:
    """Use the template below:
    Manga(
        url             = ,
        title           = ,
        author          = ,
        covers          = ,
        alt_titles      = ,
        status          = ,
        demographics    = ,
        content_rating  = ,
        genres          = ,
        updated_at      = ,
        created_at      = ,
        views           = ,
        description     = ,
        links           = ,
        chapters        = ,
    )
    """
    url             : str
    title           : str
    author          : List[str]
    covers          : List[str]                     = field(default_factory=list)
    alt_titles      : List[str]                     = field(default_factory=list)
    status          : int                           = -1
    demographics    : str                           = None
    content_rating  : str                           = None
    genres          : Dict[str, str]                = field(default_factory=dict)
    updated_at      : str                           = None
    created_at      : str                           = None
    views           : int                           = None
    description     : str                           = "No description available."
    links           : Dict[str, str]                = field(default_factory=dict)
    chapters        : Dict[Union[int, float], Ch]   = field(default_factory=dict)


def tblp(ls: List[str]):
    print(
        tabulate(
            [
                [chalk.hex("FFD166").bold(i), chalk.hex("4E8098").bold(v)]
                for i, v in enumerate(ls)
            ],
            [chalk.hex("e63946").bold("index"), chalk.hex("e76f51").bold("title")],
            tablefmt="pretty", colalign=("right", "left")
        )
    )

    return click.prompt(
        chalk.hex("3279a1").bold(
            'Enter the index of the manga to be downloaded, defaults to 0'
        ), '0',
        type=click.Choice(
            [str(i) for i in range(len(ls))]
        ),
        show_choices=False,
        show_default=False
    )


def sanitize_filename(filename: str) -> str:
    return re.sub(re.compile(r"[<>:\"/\\|?*]", re.DOTALL), "", str(filename))


def get_extension(filename: str) -> str:
    return filename.strip("/").split("/")[-1].split("?")[0].split(".")[-1]

def ordinal(n:int) -> str:
    return "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

def rc(rs: str):
    for matches in re.finditer(r"(?:([-]*[0-9]*.[0-9]*)[:]([-]*[0-9]*.[0-9]*)|([-]*[0-9]+.[0-9]*))", rs):
        start, end, singular = matches.groups()
        if ((start or '').isdigit() and (end or '').isdigit()) and float(start) > float(end):
            start, end = end, start
        yield (lambda x, s=singular: float(s) == x) if singular else (lambda x: True) if not (start or end) else (lambda x, s=start: x >= float(s)) if start and not end else (lambda x, e=end: x <= float(e)) if not start and end else (lambda x, s=start, e=end: float(s) <= x <= float(e))

def cr(rs: str):
    if not rs:
        return lambda *args, **kwargs: True
    return lambda x: any(condition(x) for condition in rc(rs))

# class Downloader:
#     def __init__(self, title: str, ra: Callable[[httpx.Response], int]=None, ddir: str=None, **kwargs: dict[str, Any]):
#         self.title = title
#         if ddir:
#             self.ddir = ddir
#         elif sys.platform == "win32":
#             self.ddir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
#         else:
#             self.ddir = os.path.join(os.path.expanduser('~'), "Manga")
#         self.ra = ra
#         ls = [
#             "delfolder",
#             "format",
#             "overwrite",
#             "retry",
#             "retryprompt",
#             "threads",
#         ]
#         for i in ls:
#             setattr(self, i, kwargs[i])

#     def _dlf(self, file: str, n: int=0):
#         if (n+1) == self.retry:
#             if self.retryprompt:
#                 log.warning(f"Download failed for {ordinal(self.retry)} time, will prompt the user.", "downloader")
#                 if click.prompt(f"Download failed for {ordinal(self.retry)} time, do you want to continue the download? (y | n). Defaults to y", "y", type=click.Choice(["y", "n"]), show_choices=False, show_default=False) == "y":
#                     log.info(f"Download will be retried again", "downloader")
#                     self._dlf(file, 0,)
#                 else:
#                     log.info(f"Download is not retried, will skip.", "downloader")
#             else:
#                 log.error(f"Download failed for {ordinal(self.retry)} time, will halt the download.", "downloader")
#         else:
#             if n:
#                 log.warning(f"Download failed for the {ordinal(n)} time, will retry.", "downloader")
#             with open(file[0] + ".tmp", "wb") as f:
#                 try:
#                     with httpx.stream("GET", file[1], **self.kwargs) as r:
#                         for chunk in r.iter_bytes(chunk_size=8192):
#                             f.write(chunk)
#                 except (httpx.ReadTimeout, httpx.ConnectTimeout):
#                     self._dlf(file, n+1)

#     def dlf(self, file: tuple[str, str]):
#         try:
#             os.makedirs(os.path.split(file[0])[0])
#         except FileExistsError:
#             pass

#         if os.path.isfile(f"{file[0]}.tmp"):
#             os.remove(f"{file[0]}.tmp")

#         if self.overwrite or not os.path.isfile(file[0]):
#             log.info(f"Overwriting {file[0]}." if os.path.isfile(file[0]) else f"Downloading {file[0]}.", "downloader")
#             self._dlf(file)
#             os.replace(f"{file[0]}.tmp", file[0])
#         else:
#             log.debug(f"Skipping {file[0]}", "downloader")

#     def dlch(self, chapter_name: str, pages: list[str], **kwargs: dict[str, Any]):
#         jdir = os.path.join(self.ddir, self.title, sanitize_filename(chapter_name))
#         fm = self.format.lower()
#         dl = True
#         if not self.overwrite:
#             if os.path.isdir(jdir):
#                 log.debug(f"Skipping {jdir} as it exists and overwrite flag is not raised.", "downloader")
#                 dl = False
#             elif os.path.isfile(f"{jdir}.{fm}"):
#                 log.debug(f"Skipping {jdir}.{fm} as it exists and overwrite flag is not raised.", "downloader")
#                 dl = False
#         if dl:
#             self.kwargs = kwargs
#             log.info(f"Downloading {chapter_name}.", "dl chapter")
#             files = []
#             for index, page in enumerate(pages):
#                 filename = os.path.join(
#                     self.ddir,
#                     self.title,
#                     sanitize_filename(chapter_name),
#                     f"{index}.{get_extension(page)}"
#                 ).replace("\\", "/")
#                 files.append((filename, page))
#             for _ in ThreadPool(self.threads).imap_unordered(self.dlf, files):
#                 pass
#             if fm != "folder":
#                 patoolib.create_archive(f"{jdir}.{fm}", [i[0] for i in files], verbosity=-1)
#                 if self.delfolder:
#                     shutil.rmtree(jdir)

# class Downloader:
#     def __init__(self, title: str, chapters: Dict[Union[float, int], List[str]], fn: Callable[[Dict[Union[float, int], str]], str], ra: Callable[[httpx.Response], int]=None, ddir: str=None, **kwargs: Dict[str, Any]):
#         self.title = title
#         self.chapters = chapters
#         self.fn = fn
#         self.ra = ra
#         if ddir:
#             self.ddir = ddir
#         elif sys.platform == "win32":
#             self.ddir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
#         else:
#             self.ddir = os.path.join(os.path.expanduser('~'), "Manga")
#         ls = [
#             "delfolder",
#             "overwrite",
#             "retry",
#             "retryprompt",
#             "threads",
#         ]
#         for i in ls:
#             setattr(self, i, kwargs[i])
#         self.format = kwargs["format"].lower()
#         self.check = cr(kwargs["range"])

#     def _dlf(self, file: str, n: int=0):
#         if (n+1) == self.retry:
#             if self.retryprompt:
#                 log.warning(f"Download failed for {ordinal(self.retry)} time, will prompt the user.", "downloader")
#                 if click.prompt(f"Download failed for {ordinal(self.retry)} time, do you want to continue the download? (y | n). Defaults to y", "y", type=click.Choice(["y", "n"]), show_choices=False, show_default=False) == "y":
#                     log.info(f"Download will be retried again", "downloader")
#                     self._dlf(file, 0,)
#                 else:
#                     log.info(f"Download is not retried, will skip.", "downloader")
#             else:
#                 log.error(f"Download failed for {ordinal(self.retry)} time, will halt the download.", "downloader")
#         else:
#             if n:
#                 log.warning(f"Download failed for the {ordinal(n)} time, will retry.", "downloader")
#             with open(file[0] + ".tmp", "wb") as f:
#                 try:
#                     with httpx.stream("GET", file[1], **self.kwargs) as r:
#                         for chunk in r.iter_bytes(chunk_size=8192):
#                             f.write(chunk)
#                 except (httpx.ReadTimeout, httpx.ConnectTimeout):
#                     self._dlf(file, n+1)

#     def dlf(self, file: tuple[str, str]):
#         try:
#             os.makedirs(os.path.split(file[0])[0])
#         except FileExistsError:
#             pass
#         if os.path.isfile(f"{file[0]}.tmp"):
#             os.remove(f"{file[0]}.tmp")
#         self._dlf(file)
#         os.replace(f"{file[0]}.tmp", file[0])

#     def dlch(self, chapter_name: str, pages: list[str]):
#         jdir = os.path.join(self.ddir, self.title, sanitize_filename(chapter_name))
#         dl = True
#         if dl:
#             log.info(f"Downloading {chapter_name}.", "dl chapter")
#             files = []
#             for index, page in enumerate(pages):
#                 filename = os.path.join(
#                     self.ddir,
#                     self.title,
#                     sanitize_filename(chapter_name),
#                     f"{index}.{get_extension(str(page))}"
#                 ).replace("\\", "/")
#                 files.append((filename, page))
#             fmt = style.t1(style.ac1(chapter_name) + " [{remaining_s:05.2f} secs, {rate_fmt:0>12}] " + style.ldb("{bar}") +" [{n:03d}/{total:03d}, {percentage:03.0f}%]")
#             with ThreadPool(self.threads) as pool:
#                 list(tqdm(pool.imap(self.dlf, files), total=len(files), leave=True, unit=" img", disable=False, dynamic_ncols=True, smoothing=1, bar_format=fmt))
#             if self.format != "folder":
#                 patoolib.create_archive(f"{jdir}.{self.format}", [i[0] for i in files], verbosity=-1)
#                 if self.delfolder:
#                     shutil.rmtree(jdir)

#     def dl(self, **kwargs: Dict[str, Any]):
#         self.kwargs = kwargs
#         for k, v in self.chapters.items():
#             dl = True
#             jdir = os.path.join(self.ddir, self.title, sanitize_filename(k))
#             if self.check(k):
#                 log.debug(f"Chapter {k} in range to be downloaded, will check if the folder/file exist and if overwrite flag is raised before proceeding to downloading the chapter.", "check")
#                 if os.path.isdir(jdir):
#                     if self.overwrite:
#                         shutil.rmtree(jdir)
#                     else:
#                         log.debug(f"Skipping {jdir} as it exists and overwrite flag is not raised.", "downloader")
#                         dl = False
#                 elif os.path.isfile(f"{jdir}.{self.format}"):
#                     if self.overwrite:
#                         os.remove(f"{jdir}.{self.format}")
#                     else:
#                         log.debug(f"Skipping {jdir}.{self.format} as it exists and overwrite flag is not raised.", "downloader")
#                         dl = False
#             if dl:
#                 self.dlch(str(k), self.fn({k: v})[1])

def downloader(
        sr: Dict[str, str],
        chs_fn: Callable[[str], List[Dict[Union[float, int, None], Any]]],
        ch_fn: Callable[[Any], List[str]],
        range: int,
        overwrite: bool,
        delfolder: bool,
        retry: int,
        retryprompt: bool,
        threads: int,
        ra: Callable[[httpx.Response], int]=None,
        headers: Dict[str, Any] = {},
        directory: str=None,
        **kwargs: Dict[str, Any]
    ):
    def _dlf(file: str, n: int=0):
        if (n+1) == retry:
            if retryprompt:
                log.warning(f"Download failed for {ordinal(retry)} time, will prompt the user.", "downloader")
                if click.prompt(f"Download failed for {ordinal(retry)} time, do you want to continue the download? (y | n). Defaults to y", "y", type=click.Choice(["y", "n"]), show_choices=False, show_default=False) == "y":
                    log.info(f"Download will be retried again", "downloader")
                    _dlf(file, 0,)
                else:
                    log.info(f"Download is not retried, will skip.", "downloader")
            else:
                log.error(f"Download failed for {ordinal(retry)} time, will halt the download.", "downloader")
        else:
            if n:
                log.warning(f"Download failed for the {ordinal(n)} time, will retry.", "downloader")
            with open(file[0] + ".tmp", "wb") as f:
                try:
                    with httpx.stream("GET", file[1], headers=headers) as r:
                        for chunk in r.iter_bytes(chunk_size=8192):
                            f.write(chunk)
                except (httpx.ReadTimeout, httpx.ConnectTimeout):
                    _dlf(file, n+1)

    def dlf(file: tuple[str, str]):
        try:
            os.makedirs(os.path.split(file[0])[0])
        except FileExistsError:
            pass
        if os.path.isfile(f"{file[0]}.tmp"):
            os.remove(f"{file[0]}.tmp")
        _dlf(file)
        os.replace(f"{file[0]}.tmp", file[0])

    if sr:
        ddir = directory
        ls = list(sr.keys())
        title = ls[int(tblp(ls))]
        _ch = chs_fn(title)
        n = 1
        chapters = {}
        for r in _ch:
            ch, arg = list(r.items())[0]
            if ch:
                k = ast.literal_eval(ch)
            else:
                k = -n
                n += 1
            chapters[k] = arg
        if ddir:
            ddir = ddir
        elif sys.platform == "win32":
            ddir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        else:
            ddir = os.path.join(os.path.expanduser('~'), "Manga")
        format = kwargs["format"].lower()
        check = cr(range)
        for k, v in chapters.items():
            dl = True
            jdir = os.path.join(ddir, title, sanitize_filename(k))
            if check(k):
                log.debug(f"Chapter {k} in range to be downloaded, will check if the folder/file exist and if overwrite flag is raised before proceeding to downloading the chapter.", "check")
                if os.path.isdir(jdir):
                    if overwrite:
                        shutil.rmtree(jdir)
                    else:
                        log.debug(f"Skipping {jdir} as it exists and overwrite flag is not raised.", "downloader")
                        dl = False
                elif os.path.isfile(f"{jdir}.{format}"):
                    if overwrite:
                        os.remove(f"{jdir}.{format}")
                    else:
                        log.debug(f"Skipping {jdir}.{format} as it exists and overwrite flag is not raised.", "downloader")
                        dl = False
            if dl:
                v = ch_fn(chapters[k])
                chapter_name = str(k)
                jdir = os.path.join(ddir, title, sanitize_filename(chapter_name))
                dl = True
                if dl:
                    log.info(f"Downloading {chapter_name}.", "dl chapter")
                    files = []
                    for index, page in enumerate(v):
                        filename = os.path.join(
                            ddir,
                            title,
                            sanitize_filename(chapter_name),
                            f"{index}.{get_extension(str(page))}"
                        ).replace("\\", "/")
                        files.append((filename, page))
                    fmt = style.t1(style.ac1(chapter_name) + " [{remaining_s:05.2f} secs, {rate_fmt:0>12}] " + style.ldb("{bar}") +" [{n:03d}/{total:03d}, {percentage:03.0f}%]")
                    with ThreadPool(threads) as pool:
                        list(tqdm(pool.imap(dlf, files), total=len(files), leave=True, unit=" img", disable=False, dynamic_ncols=True, smoothing=1, bar_format=fmt))
                    if format != "folder":
                        patoolib.create_archive(f"{jdir}.{format}", [i[0] for i in files], verbosity=-1)
                        if delfolder:
                            shutil.rmtree(jdir)
    else:
        log.debug("No manga found.", "fastdl")
        print(style.warning(f"No manga with similar title with the requested title or anything similar found. Use other search terms or remove some filters."))

class Downloader:
    def __init__(
        self,
        sr: Dict[str, str],
        chs_fn: Callable[[str], List[Dict[Union[float, int, None], Any]]],
        ch_fn: Callable[[Any], List[str]],
        ra: Callable[[httpx.Response], int]=None,
        headers: Dict[str, Any] = {},
        directory: str=None,
        **kwargs: Dict[str, Any]
    ):
        if sr:
            ak = {'range', 'overwrite', 'delfolder', 'retry', 'retryprompt', 'threads'}
            self.__dict__.update((k, v) for k, v in kwargs.items() if k in ak)
            self.__dict__.update(locals())
            ls = list(sr.keys())
            self.title = ls[int(tblp(ls))]
            _ch = chs_fn(self.title)
            n = 1
            self.chapters = {}
            for r in _ch:
                ch, arg = list(r.items())[0]
                if ch:
                    k = ast.literal_eval(ch)
                else:
                    k = -n
                    n += 1
                self.chapters[k] = arg
            if ddir:= directory:
                self.ddir = ddir
            elif sys.platform == "win32":
                self.ddir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            else:
                self.ddir = os.path.join(os.path.expanduser('~'), "Manga")
            self.format = kwargs["format"].lower()
            self.check = cr(self.range)
            for k, v in self.chapters.items():
                self.dlch(k, v)
        else:
            log.debug("No manga found.", "fastdl")
            print(style.warning(f"No manga with similar title with the requested title or anything similar found. Use other search terms or remove some filters."))

    def _dlf(self, file: str, n: int=0):
        if (n+1) == self.retry:
            if self.retryprompt:
                log.warning(f"Download failed for {ordinal(self.retry)} time, will prompt the user.", "downloader")
                if click.prompt(f"Download failed for {ordinal(self.retry)} time, do you want to continue the download? (y | n). Defaults to y", "y", type=click.Choice(["y", "n"]), show_choices=False, show_default=False) == "y":
                    log.info(f"Download will be retried again", "downloader")
                    self._dlf(file, 0,)
                else:
                    log.info(f"Download is not retried, will skip.", "downloader")
            else:
                log.error(f"Download failed for {ordinal(self.retry)} time, will halt the download.", "downloader")
        else:
            if n:
                log.warning(f"Download failed for the {ordinal(n)} time, will retry.", "downloader")
            with open(file[0] + ".tmp", "wb") as f:
                try:
                    with httpx.stream("GET", file[1], headers=self.headers) as r:
                        for chunk in r.iter_bytes(chunk_size=8192):
                            f.write(chunk)
                except (httpx.ReadTimeout, httpx.ConnectTimeout):
                    self._dlf(file, n+1)

    def dlf(self, file: tuple[str, str]):
        try:
            os.makedirs(os.path.split(file[0])[0])
        except FileExistsError:
            pass
        if os.path.isfile(f"{file[0]}.tmp"):
            os.remove(f"{file[0]}.tmp")
        self._dlf(file)
        os.replace(f"{file[0]}.tmp", file[0])

    def dlch(self, k: Union[int, float], v: List[str]):
        dl = True
        jdir = os.path.join(self.ddir, self.title, sanitize_filename(k))
        if self.check(k):
            log.debug(f"Chapter {k} in range to be downloaded, will check if the folder/file exist and if overwrite flag is raised before proceeding to downloading the chapter.", "check")
            if os.path.isdir(jdir):
                if self.overwrite:
                    shutil.rmtree(jdir)
                else:
                    log.debug(f"Skipping {jdir} as it exists and overwrite flag is not raised.", "downloader")
                    dl = False
            elif os.path.isfile(f"{jdir}.{self.format}"):
                if self.overwrite:
                    os.remove(f"{jdir}.{self.format}")
                else:
                    log.debug(f"Skipping {jdir}.{self.format} as it exists and overwrite flag is not raised.", "downloader")
                    dl = False
        if dl:
            chapter_name = str(k)
            jdir = os.path.join(self.ddir, self.title, sanitize_filename(chapter_name))
            dl = True
            if dl:
                log.info(f"Downloading {chapter_name}.", "dl chapter")
                files = []
                for index, page in enumerate(self.ch_fn(v)):
                    filename = os.path.join(
                        self.ddir,
                        self.title,
                        sanitize_filename(chapter_name),
                        f"{index}.{get_extension(str(page))}"
                    ).replace("\\", "/")
                    files.append((filename, page))
                fmt = style.t1(style.ac1(chapter_name) + " [{remaining_s:05.2f} secs, {rate_fmt:0>12}] " + style.ldb("{bar}") +" [{n:03d}/{total:03d}, {percentage:03.0f}%]")
                with ThreadPool(self.threads) as pool:
                    list(tqdm(pool.imap(self.dlf, files), total=len(files), leave=True, unit=" img", disable=False, dynamic_ncols=True, smoothing=1, bar_format=fmt))
                if format != "folder":
                    patoolib.create_archive(f"{jdir}.{self.format}", [i[0] for i in files], verbosity=-1)
                    if self.delfolder:
                        shutil.rmtree(jdir)
