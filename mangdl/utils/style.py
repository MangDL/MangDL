import itertools
from functools import partial
from typing import List

import rich
from rich.align import Align
from rich.panel import Panel
from rich.table import Column, Table
from yachalk import chalk

from ..globals import console
from .settings import stg
from .utils import ddir, dnrp


class colour:
    pass

syml = stg(stg("colour_theme"), f"{dnrp(__file__)}/styles.yaml")
cstyle = syml['colours']

for k, v in cstyle.items():
    setattr(colour, k, v)

def stylize(st: List[str], t: str):
    op = f"[{st}]{t}[/{st}]"
    return op

SA = ddir(syml, "styles/all")
t1 = chalk.hex(cstyle.pop("t1"))
ldb = chalk.hex(cstyle.pop("fg1")).bg_hex(cstyle.pop("bg1"))
for k, v in cstyle.items():
    globals()[k] = partial(stylize, f"#{v} bold")
    globals()[f"ch_{k}"] = chalk.hex(v).bold

table = ddir(syml, "styles/table")

class ct:
    def panel(text: str):
        console.print(Align.center(Panel(text, **ddir(syml, "styles/panel"), **SA)))

    def table(cols: List[str], rows: List[List[str]]):
        stb = table
        box = getattr(rich.box, stb.pop("box"))

        new_cols = []
        for title, col in zip(cols, itertools.cycle(stb.pop("columns"))):
            attr = {i: f'#{getattr(colour, col[i])}' for i in ["header_style", "style"]}
            new_cols.append(Column(title, **attr, justify="center"))

        t = Table(*new_cols, **stb, **SA, box=box)
        for i in rows:
            t.add_row(*[str(i) for i in i])

        console.print(Align.center(t))

def pprint(t):
    console.print(Align.center(t))