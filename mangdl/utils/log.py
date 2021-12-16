import inspect
import shutil
import textwrap
from datetime import datetime
from functools import partial
from threading import Lock

from yachalk import chalk

from . import style

levels = {
    "critical": "A40606",
    "error": "9c0b1d",
    "warning": "FCDC4D",
    "info": "3279a1",
    "debug": "11b180",
    "spam": "b5b5b5"
}

TERM_WIDTH = shutil.get_terminal_size((80, 20)).columns


Lock = Lock()
class logger:
    def __init__(self, vl: str):
        """
        Colorful logger?

        Args:
            td (datetime.now): epoch of the logger
            l (str): level of the message to be logged
        """
        self.td = datetime.now()
        self.vl = vl - 2
        for i in levels:
            setattr(self, i, partial(self.log, i))

    def log(self, level: str, msg: str, name: str=None):
        """
        The logger itself.

        Args:
            msg (str): message to be logged
            name (str, optional): name of the log. Defaults to None.
        """

        if self.vl >= list(levels).index(level):
            if msg:
                _, fn, ln, f, *_ = inspect.getouterframes(inspect.currentframe())[1]
                td = datetime.now() - self.td
                h, rem = divmod(td.seconds, 3600)
                m, s = divmod(rem, 60)
                td = style.t2(f"+{h:02d}:{m:02d}:{s:02d}.{td.microseconds:06d}")
                file = lambda x: style.t4(f'{fn.split("/")[-1]: <{x}}')
                func = lambda x: style.t5(f"{f: <{x}}")
                ln = style.t6(f'{ln:04d}')
                l = chalk.hex(levels[level]).bold(f"{level.upper(): <8}")
                def fmsg(x: int, indent: str=None) -> str:
                    f, *ls = textwrap.TextWrapper(width=TERM_WIDTH - x).wrap(text=str(msg))
                    if not indent:
                        n = TERM_WIDTH - (TERM_WIDTH - x)
                        indent = " " * n
                    return style.t1(f + f'\n{indent}'.join(["", *ls]))
                if TERM_WIDTH >= 150:
                    dt = style.t3(datetime.now().strftime("%H:%M:%S.%f")[:-4])
                    nm = style.t7(f"{(f'({name})' if name else ''): <18}")
                    info = f'{td}  {dt}  {file(16)}  {func(13)}  {ln}  {nm}  {l}  {fmsg(100)}'
                elif TERM_WIDTH >= 120:
                    info = f'{td} {file(15)}  {ln}  {l}  {fmsg(50)}'
                elif TERM_WIDTH >= 90:
                    info = f'{file(22)}  {ln}  {l}  {fmsg(40)}'
                else:
                    info = f'{file(0)} {ln} {fmsg(0, "    ")}'
                with Lock:
                    print(info)
