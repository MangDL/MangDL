from importlib import import_module
from typing import Any, Dict, List

from .api.base import Ch, Manga, Search


class Provider:
    def __init__(self, prov: str):
        self.prov = import_module(f".{prov}", "mangdl.api.providers")
        self.template = import_module(f".{self.prov.template}", "mangdl.api.providers.templates").template

    def chapter(self, url: str) -> Ch:
        local = locals()
        [local.pop(i) for i in ["self",]]
        return self.template(self.prov).chapter(
            **local,
        )

    def manga(self, url: str, chs: int=0) -> Manga:
        local = locals()
        [local.pop(i) for i in ["self",]]
        return self.template(self.prov).manga(
            **local,
        )

    def dl_search(self, title: str, **kwargs: Dict[str, Any]) -> Dict[str, str]:
        """Used for downloading when imported.
        Args:
            s (Search): Search dataclass, search parameters for searching.
        Returns:
            Dict[str, str]: Search results.
        """
        local = locals()
        [local.pop(i) for i in ["self",]]
        return self.template(self.prov).dl_search(
            **local,
        )

    def search(self, s: Search) -> List[Manga]:
        op = []
        for i in self.template(self.prov).dl_search(**s.__dict__).values():
            op.append(self.template.manga(i))
        return op

    def dl(self, url: str, **kwargs: Dict[str, Any]):
        local = locals()
        [local.pop(i) for i in ["self",]]
        return self.template(self.prov).dl(
            **local,
        )

    def cli_dl(self, title: str, **kwargs: Dict[str, Any]):
        local = locals()
        [local.pop(i) for i in ["self",]]
        return self.template(self.prov).cli_dl(
            **local,
        )