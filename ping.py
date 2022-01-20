import json
import time
from functools import partial
from multiprocessing.pool import ThreadPool
from operator import itemgetter
from typing import Any, Dict, List

import click
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

METHODS = ["get", "options", "head", "post", "put", "patch", "delete"]

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
        resp = getattr(httpx, method)(url, follow_redirects=True, *args, **kwargs)
        if resp.status_code == 503:
            time.sleep(2)
            return _req(url, method, *args, **kwargs)
        else:
            return resp
    except:
        time.sleep(2)
        return _req(url, method, *args, **kwargs)

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

def olp(host):
    pr = req.get(f'https://api.justyy.workers.dev/api/ping/?host={host}&cached').text
    if pr == "null":
        ping = 0
        ol = False
    else:
        try:
            ping = pr.split(r'\/')[-3]
        except:
            return olp(host)
        ol = True
    return ol, ping

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
        m, ch, dls = v["test"]
        prov = Provider(k)
        prov.manga(m)
        prov.chapter(ch)
        prov.dl_search(dls)
        for i in ["manga", "chapter", "dl_search"]:
            getattr(prov, i)
        test = True
    except:
        test = False

    ol, ping = olp(host)

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

@click.command()
@click.argument('kv')
def main(kv):
    with ThreadPool(20) as pool:
        pool.map(fping, fyml["sites"].items())
        pool.close()
        pool.join()

    req.post(f'https://{kv}.whi-ne.workers.dev', json={"ping": json.dumps(dict(sorted(op.items(), key=itemgetter(0))), indent=None)})
    console.print(Align.center(t))

if __name__ == '__main__':
    main()