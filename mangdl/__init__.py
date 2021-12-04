import importlib
from os import path
from os.path import abspath as ap
from os.path import dirname as dn

import os
from os.path import abspath as ap
from os.path import dirname as dn
from typing import Any, Dict
from zipfile import ZipFile

from .API.Base import Search

import httpx

class Error(Exception):
    pass

class IncompatibleProvider(Error):
    pass

with open(path.join(dn(ap(__file__)), "version"), "r") as cv:
    CORE_VER = cv.read()
    CORE_VER_M = int(CORE_VER.split(".")[0])

_PV = path.join(dn(ap(__file__)), "API", "Providers", "version")
if not os.path.exists(_PV):
    zfn = os.path.join(dn(ap(__file__)), "Providers.zip")
    with open(zfn, "wb") as f:
        f.write(httpx.get(f'https://codeload.github.com/MangDL/Providers/legacy.zip/refs/tags/{CORE_VER.strip()}').content)
    with ZipFile(zfn, 'r') as zip:
        for i in zip.infolist():
            path = os.path.normpath(i.filename).split(os.sep)
            fn = os.path.join("Providers", *path[1:])
            if i.filename.endswith('/'):
                os.mkdir(os.path.join(dn(ap(__file__)), fn))
            else:
                i.filename = fn
                zip.extract(i, path=os.path.join(dn(ap(__file__)), "API"))
    os.remove(zfn)
with open(_PV, "r") as pv:
    PROV_VER = pv.read()
    PROV_VER_M = int(PROV_VER.split(".")[0])

class Provider:
    def __init__(self, prov: str):
        if PROV_VER_M == CORE_VER_M:
            self.prov = importlib.import_module(f".{prov}", "mangdl.API.Providers")
        else:
            raise IncompatibleProvider(f'The providers have {"higher" if PROV_VER_M > CORE_VER_M else "lower"} version than MangDL do. Please {"down" if PROV_VER_M > CORE_VER_M else "up"}grade the providers to {CORE_VER_M}.x.x before using MangDL.')
    def dl_search(self, s: Search) -> Dict[str, str]:
        local = locals()
        [local.pop(i) for i in ["self",]]
        return self.prov.dl_search(**local)
    def dl(
        self,
        url: str,
        verbosity: int=1,
        format: str='cbz',
        delfolder: bool=True,
        threads: int=30,
        retryprompt: bool=True,
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
        range: str=None,
        cover: bool=False,
        directory: str=None,
        overwrite: bool=False,
        retry:  int=3,
        colortheme: str='whine',
        saveconfig: str=None,
        loadconfig: str=None,
        overridelc: bool=False
    ):
        print(locals())
        local = locals()
        [local.pop(i) for i in ["self",]]
        return self.prov.dl(**local)
    def cli_dl(
        self,
        verbosity: int=1,
        format: str='cbz',
        delfolder: bool=True,
        threads: int=30,
        retryprompt: bool=True,
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
        range: str=None,
        cover: bool=False,
        directory: str=None,
        overwrite: bool=False,
        retry:  int=3,
        colortheme: str='whine',
        saveconfig: str=None,
        loadconfig: str=None,
        overridelc: bool=False
    ):
        local = locals()
        [local.pop(i) for i in ["self", "verbosity", "colortheme"]]
        return self.prov.cli_dl(**local)
