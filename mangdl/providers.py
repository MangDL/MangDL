from importlib import import_module
from typing import Any, Dict, List

from .api.base import Ch, Manga


class CloudflareProtected(Exception):
    pass

class Provider:
    def __init__(self, prov: str):
        self.prov = import_module(f".{prov}", "mangdl.api.providers")
        if getattr(self.prov, "cloudflare", False):
            raise CloudflareProtected(
                f"""{prov} is protected by Cloudflare's UAM. If you know how to
                bypass Cloudflare, do a pull reqeust at
                https://github.com/MangDL/MangDL/pulls.""".replace('\n', ' ')
            )
        tpl = getattr(
            self.prov,
            "template",
            None
        )
        if tpl:
            self.template = import_module(f".{tpl}", "mangdl.api.providers.templates").template(self.prov)
        else:
            self.template = import_module(f".{prov}", "mangdl.api.providers")

    def chapter(self, url: str) -> Ch:
        local = locals()
        [local.pop(i) for i in ["self",]]
        return self.template.chapter(
            **local,
        )

    def manga(self, url: str, chs: int=0) -> Manga:
        local = locals()
        [local.pop(i) for i in ["self",]]
        return self.template.manga(
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
        return self.template.dl_search(
            **local,
        )

    def search(self, title: str, **kwargs: Dict[str, Any]) -> List[Manga]:
        local = locals()
        [local.pop(i) for i in ["self",]]
        op = []
        for i in self.template.dl_search(**local).values():
            op.append(self.template.manga(i))
        return op

    def dl(self, url: str, **kwargs: Dict[str, Any]):
        local = locals()
        [local.pop(i) for i in ["self",]]
        return self.template.dl(
            **local,
        )

    def cli_dl(self, title: str, **kwargs: Dict[str, Any]):
        local = locals()
        [local.pop(i) for i in ["self",]]
        return self.template.cli_dl(
            **local,
        )