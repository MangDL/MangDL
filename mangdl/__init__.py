import importlib
from os import path
from os.path import abspath as ap
from os.path import dirname as dn

import os
from os.path import abspath as ap
from os.path import dirname as dn
from zipfile import ZipFile

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
            fn = os.path.join("Providers", *path[1:]) + (os.sep if i.filename.endswith('/') else '')
            if i.filename.endswith('/'):
                os.mkdir(fn)
            else:
                i.filename = fn
                zip.extract(i, path=os.path.join(dn(ap(__file__)), "API"))
    os.remove(zfn)
with open(_PV, "r") as pv:
    PROV_VER = pv.read()
    PROV_VER_M = int(PROV_VER.split(".")[0])

def providers(prov: str):
    if PROV_VER_M == CORE_VER_M:
        return importlib.import_module(f".{prov}", "mangdl.API.Providers")
    else:
        raise IncompatibleProvider(f'The providers have {"higher" if PROV_VER_M > CORE_VER_M else "lower"} version than MangDL do. Please {"down" if PROV_VER_M > CORE_VER_M else "up"}grade the providers to {CORE_VER_M}.x.x before using MangDL.')
