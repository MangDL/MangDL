from yachalk import chalk

from .settings import stg
from .utils import dnrp

cstyle = stg(stg("color_theme"), f"{dnrp(__file__)}/colours.yaml")
t1 = chalk.hex(cstyle["t1"])
ldb = chalk.hex(cstyle["fg1"]).bg_hex(cstyle["bg1"])
for i in [*[f"t{i}" for i in range(2, 8)], "ac1", 'critical', 'error', 'warning', 'info', 'debug']:
    globals()[i] = chalk.hex(cstyle[i]).bold
