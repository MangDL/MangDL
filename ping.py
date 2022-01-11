import json
import time
from functools import partial
from multiprocessing.pool import ThreadPool
from operator import itemgetter
from typing import Any, Callable, Dict, List

import httpx
import yaml
from rich import box
from rich.align import Align
from rich.console import Console
from rich.table import Column, Table
from yarl import URL

from mangdl.providers import Provider
from mangdl.utils import style

console = Console()

KV_URL = "https://kv.whi-ne.workers.dev"
METHODS = ["get", "options", "head", "post", "put", "patch", "delete"]
SESSION = httpx.Client()

with open("url.yml", "r") as f:
    fyml = yaml.safe_load(f)
vm = fyml["ac"]
vn = fyml["notes"]

op = {}
top = []
cols = []

for i in ["Provider", "status", "online", "test"]:
    cols.append(Column(i, justify="center"))

t = Table(
    *cols,
    box=box.ROUNDED,
    show_lines=True,
    title_justify="center"
)

def _req(
        url: str,
        method: str = "get",
        *args: List[Any],
        **kwargs: Dict[str, Any]
    ) -> httpx.Response:
    try:
        resp = getattr(SESSION, method)(url, follow_redirects=True, *args, **kwargs)
        if resp.status_code in [503, 429]:
            time.sleep(2)
            return _req(url, method, *args, **kwargs)
    except:
        time.sleep(2)
        return _req(url, method, *args, **kwargs)
    return resp

class req:
    pass

for i in METHODS:
    setattr(req, i, partial(_req, method=i))

def ei(b: bool):
    if b:
        op = style.h4("1")
    else:
        op = style.h3("0")
    return op

def fping(item):
    k, v = item
    url = v["url"]
    host = URL(url).host
    pf = v.get("pf", "")
    notes = []
    nf = vn.get(pf)

    if nf:
        notes.append(nf)
    for i in v.get("flag", []):
        notes.append(vn.get(i))

    try:
        pn, m, ch, dls = v["test"]
        prov = Provider(pn)
        prov.manga(m)
        prov.chapter(ch)
        prov.dl_search(dls)
        for i in ["manga", "chapter", "dl_search"]:
            getattr(prov, i)
        test = True
    except:
        test = False

    pr = req.get(f'https://api.justyy.workers.dev/api/ping/?host={host}&cached').text
    if pr == "null":
        ping = 0
        ol = False
    else:
        ping = pr.split('\/')[-3]
        ol = True

    op[k] = {
        "url": url,
        "stat": ol & test,
        "ol": ol,
        "test": test,
        "ping": ping,
        "ud": int(time.time()),
        "notes": " ".join(notes),
        "pf": vm.get(pf, pf) or "N/A",
        "flag": v.get("flag", [])
    }
    t.add_row(k, ei(ol & test), ei(ol), ei(test))

with ThreadPool(20) as pool:
    pool.map(fping, fyml["sites"].items())
    pool.close()
    pool.join()

req.post(KV_URL, json={"all": json.dumps(dict(sorted(op.items(), key=itemgetter(0))), indent=None)})

console.print(Align.center(t))