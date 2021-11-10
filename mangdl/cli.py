import importlib
from typing import Any

import click
from yachalk import chalk

from .utils import globals
from .utils.log import logger
from .utils.settings import wr_stg
from .utils.utils import command

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
        getattr(importlib.import_module(f'mangdl.API.Providers.{prov if prov else "mangadex"}'), "cli_dl")(title, **kwargs)

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