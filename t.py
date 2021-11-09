from mangdl.API.Base import soup
from mangdl.utils.utils import ddir

import json

s = soup("https://catmanga.org/series/abyss")

print(ddir(json.loads(s.select_one("#__NEXT_DATA__").text), "props/pageProps/series/chapters"))
