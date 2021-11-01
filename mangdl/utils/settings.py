import json
from os import path
from os.path import abspath as ap
from os.path import dirname as dn
from typing import Any

import toml
import yaml


def readcfg(file: str):
    with open(file, "r") as f:
        d = {
            "json": lambda f: json.load(f),
            "yaml": lambda f: yaml.load(f.read(), yaml.FullLoader),
            "toml": lambda f: toml.load(f)
        }
        return d[file.split(".")[-1]](f)


def stg(stg: str, file: str = path.join(dn(ap(__file__)), "settings.json")) -> Any:
    op = readcfg(file)
    if stg is not None:
        for a in stg.split("/"):
            op = op[a]
    return op


def wr_stg(stg: str, value: Any, file: str = path.join(dn(ap(__file__)), "settings.json")) -> None:
    stg_dict = readcfg(file)

    def modify(stg: str, value: Any, stg_dict: dict[Any:Any]):
        path_ls = stg.split("/")
        key = path_ls[0]
        if len(path_ls) > 1:
            try:
                stg_dict[key]
            except KeyError:
                stg_dict[key] = {}
            if isinstance(stg_dict[key], dict):
                modify(stg.replace(f"{key}/", ""), value, stg_dict[key])
            else:
                f_stg = '"]["'.join(stg.split("/"))
                raise Exception(f'["{f_stg}"] at {file} not found.')
        else:
            stg_dict[key] = value
            return stg_dict

    modify(stg, value, stg_dict)
    with open(path.join(dn(ap(__file__)), file), "w") as f:
        d = {
            "json": lambda f: json.dump(stg_dict, f, indent=4),
            "yaml": lambda f: yaml.dump(stg_dict, f, indent=4),
            "toml": lambda f: toml.dump(stg_dict, f)
        }
        d[file.split(".")[-1]](f)
