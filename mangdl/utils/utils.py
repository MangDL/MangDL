import ast
import builtins
import inspect
import re
from datetime import datetime, timedelta
from functools import lru_cache
from os.path import dirname as dn
from os.path import realpath as rp
from typing import Any, Callable

import click
from tabulate import tabulate

from . import exceptions
from .settings import stg


def dnrp(file: str, n: int=1) -> str:
    #FIXME: the docs aint clear
    """
    Returns the directory component of a pathname by n times.

    Args:
        file (str): File to get the directory of.
        n (int, optional): Number of times to get up the directory???? Defaults to 1.

    Returns:
        op (str): [description]
    """
    op = rp(file)
    for _ in range(n):
        op = dn(op)
    return op

def de(a: Any, d: Any) -> Any:
    """
    Defaults. Return a if a is True, else returns d.

    Args:
        a (Any): Object to be tested, will be returned if evaluates to True.
        d (Any): Default object to be returned if `a` evaluates to False.

    Returns:
        Any
    """
    if a:
        return a
    else:
        return d

def dd(default: dict[Any, Any], d: dict[Any, Any] | None):
    op = default
    if d:
        for a, v in d.items():
            op[a] = v
    return op

def ddir(d: dict[Any: Any], dir: str) -> Any:
    """Retrieve dictionary value using directory.

    Args:
        dict (dict): Dictionary to retrieve the value from.
        dir (str): Directory of the value to be retrieved.

    Returns:
        op (Any): Retrieved value.
    """
    op = d
    for a in dir.split("/"):
        op = op[a]
    return op

@lru_cache
def dt(dt: str) -> str:
    """
    Remove timezone from datetime.

    Arguments:
        dt {str} -- datetime???

    Raises:
        exceptions.UnexpectedDatetimeFormat: raised when the given string is not a datetime formatted
            at the following format: ``

    Returns:
        str -- [description]
    """
    tz = re.match(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})([-+])(\d{2}):(\d{2})", dt)
    if tz:
        iso, s, ho, mo = tz.groups()
        s = -1 if s == "-" else 1
        return (datetime.fromisoformat(iso) - (s * timedelta(hours=int(ho), minutes=int(mo)))).strftime("%Y-%m-%dT%H:%M:%S")
    elif re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", dt):
        return dt
    else:
        raise exceptions.UnexpectedDatetimeFormat(datetime)

def texc(fn:Callable[[Any], Any], exc: Callable[[Any], Any]=lambda: None, e: Exception = BaseException):
    """try except statement in a line

    Args:
        fn (function): Function to execute/catch.
        exc (function, optional): Function to executch when fn failed. Defaults to lambda:None.
        e (exception, optional): Exception to catch. Defaults to BaseException.
    """
    try:
        return fn()
    except e:
        return exc()

def cao(group: click.group, module: dict[Any, Any]):
    module = stg(f"cmd/{module}", f"{dnrp(__file__)}/config.yaml")
    arguments = module["arguments"]

    def c(f: Callable[[Any], Any]):
        s, h = module["help"]
        help = []
        if arguments:
            for k, v in arguments.items():
                arguments[k]["help"] = [*v["help"], *[None for _ in range(3 - len(v["help"]))]]
            for k, v in arguments.items():
                t, h, e = v["help"]
                e = '\nEx.: {e}' if e else ""
                help.append([f"<{k}>", t, f'{h}{e}'])
        return group.command(*de(module["args"], []), **dd({"context_settings": {'help_option_names': ['-h', '--help']}, "short_help": s, "help": f"\b\n{h}\n{tabulate(help, tablefmt='plain')}"}, module["kwargs"]))(f)

    def a(f: Callable[[Any], Any]):
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

    def o(f: Callable[[Any], Any]):
        opts = module["options"]
        if opts:
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


def command(group: click.group):
    """
    Returns a decorator for wrapping cli commands.
    """
    def inner(f: Callable[[Any], Any]):
        m = inspect.getouterframes(inspect.currentframe())[1][4][0]
        for m in cao(group, m[4:m.index("(")]):
            f = m(f)
        return f
    return inner

def parse_list(opt: str | None):
    """
    Takes a string and evaluates it to a list if it is a list,
    else it splits it into a list.

    It then evaluates the values of that list.
    """

    if type(opt) is str:
        opt = opt[1:-1]
        try:
            opts = list(ast.literal_eval(opt))
        except (SyntaxError, ValueError):
            opts = list(opt.split(','))
        for i, x in enumerate(opts):
            try:
                opts[i] = ast.literal_eval(x)
            except (SyntaxError, ValueError):
                opts[i] = x.strip()
        return opts
    else:
        return None
