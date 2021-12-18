from importlib import import_module
from typing import Any, Callable, Dict, List

from .api.base import Ch, Manga, Search
from .utils import globals
from .utils.log import logger


class Provider:
    def __init__(self, prov: str):
        self.prov = import_module(f".{prov}", "mangdl.api.providers")
    def chapter(self, url: str) -> Ch:
        """
        Return a Ch object from the given url.

        Args:
            url (str): URL of the chapter

        Returns:
            Ch
        """
        local = locals()
        [local.pop(i) for i in ["self",]]
        return self.prov.chapter(**local)
    def manga(self, url: str, chs: int=0) -> Manga:
        """Returns a Manga object from the given url.

        Args:
            url (str): URL of the manga
            chs (int): Determines whether the function return the chapters and
                its metadata (which significantly slower)(2), just the urls(1),
                or none at all(0). When given an integer other than 1-3
                (inclusive), will fallback to 1. Defaults to 0.

        Returns:
            Manga
        """
        local = locals()
        [local.pop(i) for i in ["self",]]
        return self.prov.manga(**local)
    def dl_search(self, s: Search) -> Dict[str, str]:
        """Used for downloading when imported.
        Args:
            s (Search): Search dataclass, search parameters for searching.
        Returns:
            Dict[str, str]: Search results.
        """
        local = locals()
        [local.pop(i) for i in ["self",]]
        return self.prov.dl_search(**local)
    def search(self, s: Search) -> List[Any]:
        """Can be used for searching manga when using this project as a module.

        Args:
            s (Search): Search dataclass, search parameters for searching.

        Returns:
            List[Manga]: Search results.
        """
        local = locals()
        [local.pop(i) for i in ["self",]]
        return self.prov.search(**local)
    def cli_search(
        self,
        title: str,
        verbose: int=1,
        lang: str=None,
        excludelang: str=None,
        demo: str=None,
        contentrating: str=None,
        status: str=None,
        order: str=None,
        authors: str=None,
        artists: str=None,
        year: int=None,
        includetags: str=None,
        includemode: str=None,
        excludetags: str=None,
        excludemode: str=None,
        colortheme: str='whine',
        saveconfig: str=None,
        loadconfig: str=None,
        overridelc: bool=False
    ):
        """Format click arguments and options to their respective types,
        then pass that to `dl_search` for it to return the search results.

        Args:
            title (str): Title of the manga to search for.

        Returns:
            Dict[str, str]: Search results.
        """

        local = locals()
        globals.log = logger(local.pop("verboselevel"))
        globals.style = local.pop("colortheme")
        [local.pop(i) for i in ["self",]]
        return self.prov.search(**local)
    def dl(
        self,
        url: str,
        range: str='',
        cover: bool=False,
        directory: str=None,
        overwrite: bool=True,
        format: str='cbz',
        delfolder: bool=True,
        retry: int=3,
        retryprompt: bool=False,
        threads: int=30,
    ):
        local = locals()
        [local.pop(i) for i in ["self",]]
        return self.prov.dl(**local)
    def cli_dl(
        self,
        title: str,
        **kwargs: Dict[str, Any]
    ):
        def kw(k: str, v: Any=None) -> Any:
            op = kwargs[k]
            if v:
                op = op or v
            return op
        globals.log = logger(kw("verboselevel", 4))
        globals.style = kw("colortheme", "whine")
        return self.prov.cli_dl(title, **kwargs)
