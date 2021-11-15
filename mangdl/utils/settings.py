import json
from os import path
from os.path import abspath as ap
from os.path import dirname as dn
from typing import Any

import toml
import yaml


def readcfg(file: str) -> Any:
    """Read the contents of a file with the given file name.

    Args:
        file (str): File name of the file to read the contents of.

    Returns:
        Any: The contents of the file.
    """
    with open(file, "r") as f:
        d = {
            "json": lambda f: json.load(f),
            "yaml": lambda f: yaml.load(f.read(), yaml.SafeLoader),
            "toml": lambda f: toml.load(f)
        }
        return d[file.split(".")[-1]](f)


def stg(stg: str, file: str = path.join(dn(ap(__file__)), "stg.json")) -> Any:
    """Retrieve dictionary value of the config file with the given file name
    using recursive indexing with a string.
    ex.:
        Given that settings.json contains: `{"data": {"attr": {"ch": 1}}}`
        `stg("data/attr/ch", "settings.json")` will return `1`

    Args:
        stg (str): Directory of the value to be retrieved.
        file (str, optional): File name of the file to get the value from. Defaults to `path.join(dn(ap(__file__)), "settings.json")`.

    Returns:
        Any: The retrieved value.
    """
    op = readcfg(file)
    if stg is not None:
        for a in stg.split("/"):
            op = op[a]
    return op


def wr_stg(stg: str, value: Any, file: str = path.join(dn(ap(__file__)), "stg.json")) -> None:
    """Rewrite dictionary value of the config file with the given file name
    using recursive indexing with a string.
    ex.:
        Given that settings.json contains: `{"data": {"attr": {"ch": 1}}}`
        `wr_stg("data/attr/ch", 2)`
        will rewrite settings.json to be: `{"data": {"attr": {"ch": 2}}}`

    Args:
        stg (str): Directory of the value to be rewrited.
        value (Any): Value to rewrite to.
        file (str, optional): File name of the file to rewrite the value from. Defaults to path.join(dn(ap(__file__)), "settings.json").

    Raises:
        FileNotFoundError: Raised if the file is not found.
    """
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
                raise FileNotFoundError(f'["{f_stg}"] at {file} not found.')
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
