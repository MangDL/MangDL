import os
import shutil
from os.path import abspath as ap
from os.path import dirname as dn
from typing import Any
from zipfile import ZipFile

import click
import httpx
from tabulate import tabulate
from yachalk import chalk

from .__init__ import CORE_VER_M, PROV_VER_M, IncompatibleProvider, providers
from .API.Base import req
from .utils import globals
from .utils.log import logger
from .utils.settings import wr_stg
from .utils.utils import command
import importlib

print(chalk.hex("D2748D").bold(r"""
 _____   ___     _____    _____     __   _________   ______    __
/\    ＼/   \   / ____＼ /\    ＼  /\ \ /\  ______\ /\  ___＼ /\ \
\ \ \＼   /\ \ /\ \__/\ \\ \ \＼ ＼\ \ \\ \ \_____/_\ \ \_/\ \\ \ \
 \ \ \ ＼/\ \ \\ \  ____ \\ \ \ ＼ ＼ \ \\ \ \ /\__ \\ \ \\ \ \\ \ \
  \ \ \‾‾  \ \ \\ \ \__/\ \\ \ \  ＼ ＼\ \\ \ \\/__\ \\ \ \\_\ \\ \ \____
   \ \_\    \ \_\\ \_\ \ \_\\ \_\＼ ＼____\\ \________\\ \_____/ \ \_____\
    \/_/     \/_/ \/_/  \/_/ \/_/  ＼/____/ \/________/ \/____/   \/_____/

The most inefficient, non user-friendly and colorful manga downloader (and soon, also a reader)""") + chalk.hex("3279a1")('\nWIP ofc, whaddya expect?\n'))

@click.group(context_settings={'help_option_names': ['-h', '--help']})
def cli():
    """Main command group.
    """
    pass

@command(cli)
def dl(title: str, **kwargs: dict[str, Any]):
    """Download command.

    Args:
        title (str): The title of the manga to be search for and download.
    """
    print(kwargs)
    globals.log = logger(kwargs["verbosity"])
    globals.style = kwargs["colortheme"]
    sc = kwargs["saveconfig"]
    if sc:
        ls = [
            "saveconfig",
            "loadconfig",
            "overridelc"
        ]
        for i in ls:
            kwargs.pop(i)
        wr_stg(f'config/dl/{sc}', kwargs)
    else:
        prov = kwargs.pop("provider")
        try:
            providers(prov if prov else "mangadex").cli_dl(title, **kwargs)
        except IncompatibleProvider as e:
            prompt = click.confirm(f'The providers have {"higher" if PROV_VER_M > CORE_VER_M else "lower"} version than MangDL do. Do you want to {"down" if PROV_VER_M > CORE_VER_M else "up"}grade the providers to {CORE_VER_M}.x.x?')
            if prompt:
                op = []
                x = True
                i = 1
                while x:
                    resp = req.get("https://api.github.com/repos/MangDL/Providers/releases", params={"per_page": 100, "page": i}, headers={"authorization": "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"}).json()
                    x = resp != []
                    if not x:
                        break
                    for d in resp:
                        tag = d["name"]
                        if int(tag.split(".")[0]) == CORE_VER_M:
                            op.append(tag)
                    i += 1
                print(
                    tabulate(
                        [
                            [chalk.hex("D687A4").bold(k), chalk.hex("DE8E93").bold(v)] for k, v in enumerate(op)
                        ],
                        [chalk.hex("84B2BA").bold("index"), chalk.hex("8AA3DE").bold("version")],
                        tablefmt="pretty", colalign=("right", "left")
                    )
                )

                choice = click.prompt(
                    chalk.hex("3279a1").bold(
                        'Enter the index of the manga to be downloaded, defaults to 0'
                    ), '0',
                    type=click.Choice(
                        [str(i) for i in range(len(op))]
                    ),
                    show_choices=False,
                    show_default=False
                )
                choice = int(choice)
                zfn = os.path.join(dn(ap(__file__)), "Providers.zip")
                with open(zfn, "wb") as f:
                    f.write(httpx.get(f'https://codeload.github.com/MangDL/Providers/legacy.zip/refs/tags/{op[choice]}').content)
                with ZipFile(zfn, 'r') as zip:
                    shutil.rmtree(os.path.join(dn(ap(__file__)), "API", "Providers"))
                    for i in zip.infolist():
                        path = os.path.normpath(i.filename).split(os.sep)
                        fn = os.path.join("Providers", *path[1:]) + (os.sep if i.filename.endswith('/') else '')
                        i.filename = fn
                        zip.extract(i, path=os.path.join(dn(ap(__file__)), "API"))
                os.remove(zfn)
                importlib.import_module(f".{prov if prov else 'mangadex'}", "mangdl.API.Providers").cli_dl(title, **kwargs)
            else:
                raise e

@command(cli)
def credits():
    """Credits command. Display credits.
    """
    print(chalk.hex("D2748D").bold(r"""
 ______  ______  ______  _____   __  ______  ______
/\  ___\/\  == \/\  ___\/\  __-./\ \/\__  _\/\  ___\
\ \ \___\ \  __<\ \  __\\ \ \/\ \ \ \/_/\ \/\ \___  \
 \ \_____\ \_\ \_\ \_____\ \____-\ \_\ \ \_\ \/\_____\
  \/_____/\/_/ /_/\/_____/\/____/ \/_/  \/_/  \/_____/""") + chalk.hex("11b180").bold("\n\nThank you:") + chalk.hex("3279a1")("""\n
- To Arjix, who helped me in implementing majority of the features and de-minifying
  my code, making it more readable and more efficient at the same time
- To KR, who let me use the KR-naming scheme like "AnimDL" do
- To whi~nyaan, my alter ego, for just existing (and purring, ofc)
- And to everyone who supported me from the very beginning of this humble
  project to its release!\n"""))
