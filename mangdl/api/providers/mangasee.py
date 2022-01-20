import ast
from functools import lru_cache, partial
import json
import re
from typing import Any, Dict, List, Union

from mangdl.utils.utils import dt, sanitize_text

from ..base import Ch, Downloader, Manga, soup

base_url = "https://mangasee123.com"

@lru_cache
def chj(url: str):
    resp = soup(url).select("script")[-1].text
    return json.loads(re.findall(r"vm\.Chapters = .+}];", resp)[0][14:-1])

@lru_cache
def cuc(url: str) -> str:
    rch, *idx = ".".join(url.split("-chapter-")[-1].split(".")[:-1]).split("-")
    return ast.literal_eval(rch), f'{"0" if len(idx) else "1"}{(str(float(rch)).replace(".", "")).zfill(5)}'

def chapter(url):
    ms = soup(url)
    ch, rcuc = cuc(url)
    rchj = chj(f'{base_url}{soup(url).select_one("a.btn-sm")["href"]}')
    for i in rchj:
        if rcuc == i["Chapter"]:
            ch_dict = i
            break
    print(ch_dict)
    return Ch(
        url             = url,
        ch              = ch,
        title           = f'Chapter {ch}',
        uploaded_at     = dt(ch_dict["Date"], r'%Y-%m-%d %H:%M:%S'),
        imgs            = [i["src"] for i in soup(url).select(".img-fluid")]
    )

@lru_cache
def clc(title: str, code: str) -> str:
    a = code[5: 6]
    if a == "0":
        p = ''
    else:
        p = f'.{a}'
    ch = f'{int(str(code)[1: 5])}{p}'
    return ch, "https://mangasee123.com/read-online/{}-chapter-{}{}.html".format(
        title,
        ch,
        (lambda a: ('' if a == '1' else f'-index-{a}'))(code[:1]),
    )

def chdls(url: str, chs: int=0) -> List[Dict[Union[float, int, None], str]]:
    ms = soup(url)
    op = []
    if chs:
        clcp = partial(clc, ms.select_one(".list-group-item h1").text)
        rchj = chj(url)
        for c in rchj:
            ch, cch = clcp(c["Chapter"])
            if chs == 2:
                cch = chapter(cch)
            op.append({ch: cch})
    return op

def manga(url, chs=0):
    ms = soup(url)
    mdj = json.loads(sanitize_text(ms.select_one('[type="application/ld+json"]').text))['mainEntity']
    md = {i.text: i for i in ms.select("li.list-group-item span.mlabel")}

    rs = md["Status:"].find_parent().select("a")[1].text.lower().split()[0]
    status = -1
    for k, v in enumerate([["ongoing",], ["completed",], ["hiatus",], ["cancelled", "discontinued"]]):
        if rs in v:
            status = k
            break
    genres = {}
    for i in md["Genre(s):"].find_parent().select("a"):
        genres[sanitize_text(i.text)] = f"{base_url}{i['href']}"
    return Manga(
        url             = url,
        title           = ms.select_one(".list-group-item h1").text,
        author          = mdj["author"],
        covers          = [ms.select_one(".col-md-3 img")["src"]],
        alt_titles      = mdj["alternateName"],
        status          = status,
        genres          = genres,
        updated_at      = dt(mdj["dateModified"], r"%Y-%m-%d %H:%M:%S"),
        created_at      = dt(mdj["datePublished"], r"%Y-%m-%d %H:%M:%S"),
        description     = ms.select_one("div.top-5 .Content").text,
        chapters        = chdls(url, chs),
    )

def dl_search(title: str, **kwargs: Dict[str, Any]) -> Dict[str, str]:
    title = re.sub(r'[^A-Za-z0-9 ]+', '', title).replace(" ", "_")
    sr = {}
    ms = soup(f"https://manganato.com/search/story/{title}")
    gp = ms.select_one(".group-page")
    if gp:
        for p in range(len(gp.select("a")) - 2):
            for r in soup(f"https://manganato.com/search/story/hello?page={p+1}").select(".a-h.text-nowrap.item-title"):
                sr[r["title"]] = r["href"]
    else:
        for r in ms.select(".a-h.text-nowrap.item-title"):
            sr[r["title"]] = r["href"]
    return sr

def cli_search(title: str, **kwargs: Dict[str, Any]):
    return dl_search(title, **kwargs)

def ch_fn(url: str) -> List[str]:
    return [i["src"] for i in soup(url).select(".container-chapter-reader img")]

def dl(url: str, **kwargs: Dict[str, Any]):
    Downloader(ch_fn, headers={"Referer": "https://readmanganato.com/"}, **kwargs).dl_chdls(chdls(url), soup(url).select_one(".story-info-right h1").text)

def cli_dl(title: str, **kwargs: Dict[str, Any]):
    Downloader(ch_fn, headers={"Referer": "https://readmanganato.com/"}, **kwargs).cli(cli_search, chdls, title)
