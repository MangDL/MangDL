from types import ModuleType
from typing import Any, Dict, List, Union

from ...base import Ch, Manga


class template:
    def __init__(self, prov: ModuleType) -> None:
        self.prov = prov

    def ch_fn(self, url: str) -> List[str]:
        local = locals()
        [local.pop(i) for i in ["self",]]
        return self.prov.ch_fn(**local)

    def chapter(self, url: str) -> Ch:
        local = locals()
        [local.pop(i) for i in ["self",]]
        return self.prov.chapter(**local)

    def chdls(self, url: str, chs: int=0) -> List[Dict[Union[float, int, None], str]]:
        local = locals()
        [local.pop(i) for i in ["self",]]
        return self.prov.chdls(**local)

    def manga(self, url: str, chs: int=0) -> Manga:
        local = locals()
        [local.pop(i) for i in ["self",]]
        return self.prov.manga(**local)

    def dl_search(self, title: str, **kwargs: Dict[str, Any]):
        return self.prov.dl_search(title, **kwargs)

    def cli_search(self, title: str, **kwargs: Dict[str, Any]) -> Dict[str, str]:
        local = locals()
        [local.pop(i) for i in ["self",]]
        return self.prov.clu_search(**local)

    def dl(self, url: str, **kwargs: Dict[str, Any]):
        local = locals()
        [local.pop(i) for i in ["self",]]
        return self.prov.dl(**local)

    def cli_dl(self, title: str, **kwargs: Dict[str, Any]):
        local = locals()
        [local.pop(i) for i in ["self",]]
        return self.prov.cli_dl(**local)