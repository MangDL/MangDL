import builtins
import inspect
from typing import Any, Callable, List

import click
from tabulate import tabulate
from yachalk import chalk

from .providers import Provider
from .utils.settings import stg
from .utils.utils import dd, de, dnrp

print(chalk.hex("D2748D").bold(r"""
 _____   ___     _____    _____     __   _________   ______    __
/\    ＼/   \   / ____＼ /\    ＼  /\ \ /\  ______\ /\  ___＼ /\ \
\ \ \＼   /\ \ /\ \__/\ \\ \ \＼ ＼\ \ \\ \ \_____/_\ \ \_/\ \\ \ \
 \ \ \ ＼/\ \ \\ \  ____ \\ \ \ ＼ ＼ \ \\ \ \ /\__ \\ \ \\ \ \\ \ \
  \ \ \‾‾  \ \ \\ \ \__/\ \\ \ \  ＼ ＼\ \\ \ \\/__\ \\ \ \\_\ \\ \ \____
   \ \_\    \ \_\\ \_\ \ \_\\ \_\＼ ＼____\\ \________\\ \_____/ \ \_____\
    \/_/     \/_/ \/_/  \/_/ \/_/  ＼/____/ \/________/ \/____/   \/_____/

The most inefficient, non user-friendly and colorful manga downloader (and soon, also a reader)""") + chalk.hex("3279a1")('\nChat with whi~nyaan at https://discord.com/invite/JbAtUxGcJZ\n'))

def cao(group: click.group, cmd: str) -> List[Callable[[Callable[[Any], Any]], Callable[[Any], Any]]]:
    """Retruns wrappers for a click command evaluated from the given arguments.

    Args:
        group (click.group): Command group of the command to be under.
        cmd (str): Name of the command.

    Returns:
        List[Callable[[Callable[[Any], Any]], Callable[[Any], Any]]]: The wrappers.
    """
    cmd = stg(f"cmd/{cmd}", f"{dnrp(__file__)}/utils/config.yaml")
    arguments = cmd["arguments"]

    def c(f: Callable[[Any], Any]) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """The command wrapper.
        Args:
            f (Callable[[Any], Any]): The command function to be decorated.
        Returns:
            Callable[[Callable[[Any], Any]], Callable[[Any], Any]]
        """
        help = []
        if arguments:
            for k, v in arguments.items():
                arguments[k]["help"] = [*v["help"], *[None for _ in range(3 - len(v["help"]))]]
            for k, v in arguments.items():
                t, h, e = v["help"]
                e = '\nEx.: {e}' if e else ""
                help.append([f"<{k}>", t, f'{h}{e}'])
        s, h = cmd["help"]
        return group.command(*de(cmd["args"], []), **dd({"context_settings": {'help_option_names': ['-h', '--help']}, "short_help": s, "help": f"\b\n{h}\n{tabulate(help, tablefmt='plain')}"}, cmd["kwargs"]))(f)

    def a(f: Callable[[Any], Any]) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """The arguments wrapper.
        Args:
            f (Callable[[Any], Any]): The command function to be decorated.
        Returns:
            Callable[[Callable[[Any], Any]], Callable[[Any], Any]]
        """
        args = {}
        kwargs = {}
        if arguments:
            for k, v in arguments.items():
                kw = {"metavar": f"<{k}>"}
                args[k] = [k, *de(v["args"], [])]
                kwargs[k] = dd(kw, v["kwargs"])
            for i in list(args.keys()):
                f = click.argument(*args[i], **kwargs[i])(f)
        return f

    def o(f: Callable[[Any], Any]) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """The options wrapper.
        Args:
            f (Callable[[Any], Any]): The command function to be decorated.
        Returns:
            Callable[[Callable[[Any], Any]], Callable[[Any], Any]]
        """
        if opts:= cmd["options"]:
            n = 0
            args = {}
            kwargs = {}
            for k, v in opts.items():
                l = len(v["help"][0] or "")
                n = l if l > n else n
                opts[k]["help"] = [*v["help"], *[None for _ in range(3 - len(v["help"]))]]
            for k, v in opts.items():
                a = de(v["args"], [])
                kw = de(v["kwargs"], {})
                a[0] = f"--{a[0]}"
                a.insert(0, f"-{k}")
                kt = kw.get("type", None)
                t, h, e = v["help"]
                t = t or ""
                h = "\n".join(f'{" " * ((n + 3)-(0 if i else len(j)))}{j}' for i, j in enumerate(h.split("\n"))) if h else ""
                e = "\n" + "\n".join(f'{" " * (n + (11 if i else 5))}{"Ex.: " if not i else ""}{j}' for i, j in enumerate(e.split("\n"))) if e else ""
                kw["help"] = f'\b\n{t}{" "*((n + 3) - len(t))}{h}{e}'
                if type(kt) is dict:
                    ktk, ktv = list(kt.items())[0]
                    kta, ktkw = [i[1] for i in ktv.items()]
                    kw["type"] = getattr(click, ktk)(*kta, **ktkw if ktkw else {})
                elif kt:
                    kw["type"] = getattr(builtins, kt)
                args[k] = a
                kwargs[k] = kw
            for i in list(args.keys()):
                f = click.option(*args[i], **kwargs[i])(f)
        return f

    return c, a, o

def command(group: click.group) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
    """Wrapper for click commands.

    Args:
        group (click.group): Command group of the command to be under.

    Returns:
        Callable[[Callable[[Any], Any]], Callable[[Any], Any]]
    """
    def inner(f: Callable[[Any], Any]):
        m = inspect.getouterframes(inspect.currentframe())[1][4][0]
        for m in cao(group, m[4:m.index("(")]):
            f = m(f)
        return f
    return inner

@click.group(context_settings={'help_option_names': ['-h', '--help']})
def cli():
    """
    Main command group.
    """
    pass

@command(cli)
def dl(title: str, **kwargs: dict[str, Any]):
    """Download command.

    Args:
        title (str): The title of the manga to be search for and download.
    """
    Provider(kwargs.pop("provider", "mangadex")).cli_dl(title, **kwargs)

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
