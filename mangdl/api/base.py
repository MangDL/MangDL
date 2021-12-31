import ast
import os
import re
import shutil
import sys
import time
from dataclasses import dataclass, field
from functools import partial
from multiprocessing.pool import ThreadPool
from typing import Any, Callable, Dict, List, Type, Union

import click
import httpx
import patoolib
from bs4 import BeautifulSoup
from tabulate import tabulate
from tqdm import tqdm
from yachalk import chalk
from yarl import URL

from ..utils import style
from ..utils.exceptions import DownloadFailed

METHODS = ["get", "options", "head", "post", "put", "patch", "delete"]
SESSION = httpx.Client()

def _req(
        url: str,
        ra: Callable[[httpx.Response], int]=None,
        method: str = "get",
        session: httpx.Client = SESSION,
        *args: List[Any],
        **kwargs: Dict[str, Any]
    ) -> httpx.Response:
    """Custom request function with retry after capabilities for 429s.

    Args:
        url (str): URL to send the request to.
        ra (Callable[[httpx.Response], int], optional): Retry after function,
            receives the Response object and returns the seconds before
            retrying. Defaults to None.
        method (str, optional): The request method. Defaults to "get".
        session (httpx.Client, optional): Session client. Defaults to SESSION.

    Returns:
        httpx.Response: Response object.
    """
    resp = getattr(session, method)(url, follow_redirects=True, *args, **kwargs)
    if resp.status_code == 429:
        if ra:
            time.sleep(ra(resp))
            return _req(url, ra, method, session, *args, **kwargs)
    return resp

class req:
    pass

class ddos_guard:
    pass

ddos_resp = httpx.post("https://check.ddos-guard.net/check.js")
ddos_cookies = {k: v for k, v in ddos_resp.cookies.items()}
ddos_session = httpx.Client(cookies=ddos_cookies)

req_dict = {
    req: {},
    ddos_guard: {"session": ddos_session},
}

for r, kw in req_dict.items():
    for i in METHODS:
        setattr(r, i, partial(_req, method=i, **kw))

def soup(url: str, req: Type[req]=req, method: str="get", **kwargs: Dict[str, Any]) -> BeautifulSoup:
    """Returns a soup from the given url.

    Args:
        url (str): URL to get the soup from.
        req (Type[req], optional): Object to call the methods from. Defaults to req.

    Returns:
        BeautifulSoup: the soup
    """
    return BeautifulSoup(getattr(req, method)(url, **kwargs).text, "lxml")

@dataclass
class Vls:
    vdict   : Dict[str, Any]
    ls      : List[str]

@dataclass
class Ch:
    url              : str
    ch               : Union[int, float, None]
    vol              : Union[int, float, None]
    title            : str
    views            : int                      = 0
    uploaded_at      : str                      = None
    scanlator_groups : List[str]                = field(default_factory=list)
    user             : str                      = None
    imgs             : List[str]                = field(default_factory=list)


@dataclass
class Manga:
    url             : str
    title           : str
    author          : List[str]
    artist          : List[str]                     = field(default_factory=list)
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
    chapters        : Dict[Union[int, float], Ch]   = field(default_factory=list)


def tblp(ls: List[str], ct: str="title", prompt: str='Enter the index of the manga to be downloaded'):
    """Table prompt.
    Receive a list of items, format it in a table form and print,
    then prompt the user to choose from the list using an index.

    Args:
        ls (List[str]): List of items.
        ct (str, optional): [description]. Defaults to "title".
        prompt (str, optional): [description]. Defaults to 'Enter the index of the manga to be downloaded'.

    Returns:
        click.prompt: The input of the user.
    """
    print(
        tabulate(
            [
                [chalk.hex("FFD166").bold(i), chalk.hex("4E8098").bold(v)]
                for i, v in enumerate(ls)
            ],
            [chalk.hex("e63946").bold("index"), chalk.hex("e76f51").bold(ct)],
            tablefmt="pretty", colalign=("right", "left")
        )
    )

    return click.prompt(
        chalk.hex("3279a1").bold(
            f'{prompt}, defaults to 0'
        ), '0',
        type=click.Choice(
            [str(i) for i in range(len(ls))]
        ),
        show_choices=False,
        show_default=False
    )


def sanitize_filename(filename: str) -> str:
    """Sanitize the given filename.

    Args:
        filename (str): The filename to be sanitized.

    Returns:
        str: Sanitized filename.
    """
    return re.sub(re.compile(r"[<>:\"/\\|?*]", re.DOTALL), "", str(filename))


def get_extension(filename: str) -> str:
    """Get the file extension of a file from the given filename.

    Args:
        filename (str): The filename to get the file extension from.

    Returns:
        str: The file extension from the given filename.
    """
    return filename.strip("/").split("/")[-1].split("?")[0].split(".")[-1]

def ordinal(n: int) -> str:
    """Convert the given number to ordinal number.

    Args:
        n (int): The number to convert into ordinal number.

    Returns:
        str: The said ordinal number.
    """
    return "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

def _cr(rs: str):
    """The function that calculates the range.

    Args:
        rs (str): The range string where the range is calculated from.

    Yields:
        Callable[[Any], bool]: The function that checks if the given int is within the range or not.
    """

    for matches in re.finditer(r"(?:(-?[0-9.]*)[:](-?[0-9.]*)|(-?[0-9.]+))", rs):
        start, end, singular = matches.groups()
        if (start and end) and float(start) > float(end):
            start, end = end, start
        yield (lambda x, s=singular: float(s) == x) if singular else (lambda x: True) if not (start or end) else (lambda x, s=start: x >= float(s)) if start and not end else (lambda x, e=end: x <= float(e)) if not start and end else (lambda x, s=start, e=end: float(s) <= x <= float(e))
    if not rs:
        return lambda *args, **kwargs: True

def cr(rs: str) -> Callable[[int], bool]:
    """Returns a function that checks if the given int is within the range or not.
    The range is calculated from the given string.

    Args:
        rs (str): The range string where the range is calculated from.

    Returns:
        Callable[[int], bool]: The function that checks if the given int is within the range or not.
    """


    if rs:
        return lambda x: any(condition(x) for condition in _cr(rs))
    else:
        return lambda x: True


class Downloader:
    def __init__(
        self,
        ch_fn: Callable[[Any], List[str]],
        ra: Callable[[httpx.Response], int]=None,
        headers: Dict[str, Any] = {},
        range: str='',
        directory: str=None,
        overwrite: bool=True,
        format: str='cbz',
        delfolder: bool=True,
        retry: int=3,
        retryprompt: bool=False,
        threads: int=30,
        **kwargs: Dict[str, Any]
    ):
        local = locals()
        for i in ["ch_fn", "ra", "headers", "overwrite", "delfolder", "retry", "retryprompt", "threads"]:
            setattr(self, i, local[i])
        if ddir:= directory:
            self.ddir = ddir
        elif sys.platform == "win32":
            self.ddir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', 'Manga')
        else:
            self.ddir = os.path.join(os.path.expanduser('~'), "Manga")
        self.format = format.lower()
        self.check = cr(range)

    def _dlf(self, file: list[str], n: int=0):
        """The core individual image downloader.

        Args:
            file (str): List containing the filename and the url of the file.
            n (int, optional): Times the download for this certain file is retried. Defaults to 0.
        """
        if (n+1) == self.retry:
            return False
        else:
            with open(file[0] + ".tmp", "wb") as f:
                try:
                    with httpx.stream("GET", file[1], headers=self.headers) as r:
                        if r.status_code == 200:
                            for chunk in r.iter_bytes(chunk_size=8192):
                                f.write(chunk)
                        elif r.status_code == 429:
                            retry = self.ra(r)
                            time.sleep(retry)
                            self._dlf(file, n)
                except (httpx.ReadTimeout, httpx.ConnectTimeout):
                    self._dlf(file, n+1)
            return True

    def dlf(self, file: List[str]):
        """Individual image downloader.

        Args:
            file (str): List containing the filename and the url of the file.
        """
        try:
            os.makedirs(os.path.split(file[0])[0])
        except FileExistsError:
            pass
        if os.path.isfile(f"{file[0]}.tmp"):
            os.remove(f"{file[0]}.tmp")
        f = self._dlf(file)
        if f:
            os.replace(f"{file[0]}.tmp", file[0])
        else:
            raise DownloadFailed(f"Download of {file[1]} failed.")

    def dlch(self, k: Union[int, float], v: List[str], n: int=0):
        """Individual chapter downloader.

        Args:
            k (Union[int, float]): Chapter number.
            v (List[str]): List of image urls.
        """
        dl = True
        jdir = os.path.join(self.ddir, self.title, sanitize_filename(k))
        if self.check(k):
            if os.path.isdir(jdir):
                if self.overwrite:
                    shutil.rmtree(jdir)
                else:
                    dl = False
            if os.path.isfile(f"{jdir}.{self.format}"):
                if self.overwrite:
                    os.remove(f"{jdir}.{self.format}")
                else:
                    dl = False
        if (n+1) == self.retry:
            dl = False
        if dl:
            chapter_name = str(k)
            jdir = os.path.join(self.ddir, self.title, sanitize_filename(chapter_name))
            dl = True
            if dl:
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
                try:
                    with ThreadPool(self.threads) as pool:
                        list(tqdm(pool.imap(self.dlf, files), total=len(files), leave=True, unit=" img", disable=False, dynamic_ncols=True, smoothing=1, bar_format=fmt))
                except DownloadFailed as e:
                    if self.retryprompt:
                        self.dlch(k, v, n+1)
                    else:
                        raise e

                if self.format != "folder":
                    patoolib.create_archive(f"{jdir}.{self.format}", [i[0] for i in files], verbosity=-1)
                    if self.delfolder:
                        shutil.rmtree(jdir)

    def dl(self, title: str, chs: Dict[Union[int, float], list[str]]):
        self.title = title
        for k, v in chs.items():
            self.dlch(k, v)

    def dl_chdls(
        self,
        chdls: List[Dict[Union[float, int, None], str]],
        title: str,
    ):
        n = 1
        chs = {}
        for r in chdls:
            ch, arg = list(r.items())[0]
            if ch:
                if type(ch) is int or type(ch) is float:
                    k = ch
                else:
                    k = ast.literal_eval(ch)
            else:
                k = -n
                n += 1
            chs[k] = arg
        self.dl(title, chs)

    def cli(
        self,
        cli_search: Callable[[str], Dict[str, str]],
        chdls: Callable[[str], List[Dict[Union[float, int, None], str]]],
        title: str,
    ):
        sr = cli_search(title)
        if sr:
            ls = list(sr.keys())
            title = ls[int(tblp(ls))]
            self.dl_chdls(chdls(sr[title]), title)
        else:
            print(style.warning(f"No manga with similar title with the requested title or anything similar found. Use other search terms or remove some filters."))

def urel(url: str):
    url = URL(url)
    if url.is_absolute():
        url = url.relative()
    return url