<h1 align="center" style="font-weight: bold">
    CHANGELOG
</h1>

## **MangDL v.2.0.1**

### **CHANGED**

- Removed `search` function in `mangdl/api/providers/templates/guya.py`, `mangdl/api/providers/mangadex.py`, and `mangdl/api/providers/manganato.py`.

### **FIXED**

- Removed `from ...base import Search` in `mangdl/api/providers/templates/guya.py`.
- Removed `from ..base import Search` in `mangdl/api/providers/mangadex.py` and `mangdl/api/providers/manganato.py`.
- Fixed description metadata in `mangdl/api/providers/templates/wordpress.py`'s `manga` function to output "No description available." when the description is not available.
- Fixed `cli_search` in `mangdl/api/providers/mangadex.py` and `mangdl/api/providers/manganato.py` to return `dl_search(title, **params)` instead of `dl_search(Search(title, **params))`.
- Fixed `scanlator` in `mangdl/api/providers/setsuscans.py` to be assigned the value of "Setsu Scans" instead of "Paean Scans".
- Fixed `mangdl/providers.py`'s `Provider` class' `init` function to import the right thing.

## **MangDL v.2.0.0**

NOW, THIS IS A PROVIDER SPREE!

### **ADDED**

- <a target="_blank" href="https://www.cmreader.info">Chibimanga</a> provider

- <a target="_blank" href="https://1stkissmanga.io">1ST Kiss MANGA</a> provider

- <a target="_blank" href="https://mangakomi.com">Manga Komi</a> provider

- <a target="_blank" href="https://mangazuki.me">manga ZUKI</a> provider

- <a target="_blank" href="https://vinload.com">vinmanga</a> provider

- <a target="_blank" href="https://zinmanga.com">Zinmanga</a> provider

### **CHANGED**

- `cloudflare` must be set to `True` in the provider script if the said provider is protected by cloudflare's UAM. This is in case a method of bypassing it has been found out.
d
- Use `generic` as a template for providers who does not use a template.

- Removed `Search` dataclass. You can now use `search` function without passing it, instead you pass the arguments directly.

- `dt` function in `utils/utils.py` will now "dehumanize" the datetime passed if it contains the word "ago".

- `provider` option for the CLI commands does not verify the input now.

## **MangDL v.1.0.1**

### **FIXED**

- `setup.py` fixed as the pip installation for Windows OS not working due to the said OS apparently reading the `docs/README.md` in `cp1252` encoding instead of `utf-8`

## **MangDL v.1.0.0**

### **ADDED**

- <a target="_blank" href="https://xunscans.xyz">Xun Scans</a> provider
- Description metadata for providers using the wordpress template.

### **FIXED**

- Title of the search results from the providers using the wordpress template.

## **MangDL v.1.0.0-alpha.1**

### **ADDED**

- `__main__.py` so MangDL cli can be used when installed programmatically.

## **MangDL v.1.0.0-alpha.0**

### **ADDED**

- Templates for sites that uses Wordpress and other variants, and <a target="_blank" href="https://github.com/appu1232/guyamoe">guya.moe</a> manga reading framework.

### **CHANGED**

- Rewrote provider scripts to use a template if they have one.

### **FIXED**

- Lack of manganato provider script's `dl_search` function (literally wondering right now how that script works despite lacking one).
- mangadex provider script's `dl_search` fixed to accept `title` and kwargs instead of just a `Search` dataclass.

## **MangDL v.0.1.0**

### **ADDED**

- <a target="_blank" href="https://paeanscans.com">Paean Scans</a> provider

### **CHANGED**

- Removed light novel checking for Mangasushi and Ace Scans provider scripts.

## **MangDL v.0.0.1**

### **ADDED**

- <a target="_blank" href="https://mangasushi.net">Mangasushi</a> provider

### **CHANGED**

- Refactor Setsu Scans' manga function.

### **FIXED**

- Replace the version number in the `setup.py` to reflect the real version of the app.
- Remove the line that imports the non-standard regex library in `mangdl/api/base.py`.

## **MangDL v.0.0.0-beta.1**

### **ADDED**

- <a target="_blank" href="https://setsuscans.com">Setsu Scans</a> provider

### **CHANGED**

- Removed logging.

### **FIXED**

- Mangadex provider (I actually forgot what I fixed there, don't ask me and my shitty memory).

## **MangDL v.0.0.0-beta.0**

### **ADDED**

- Scripts for setting up portable packages in Windows.

### **FIXED**
- Windows packages should now work.

## **MangDL v.0.0.0-alpha.4**

### **ADDED**

- Installation and download scripts for linux and windows packages. Instructions coming soon!

### **FIXED**

- Windows packages should now work

## **MangDL v.0.0.0-alpha.3**

FIRST PACKAGE PRERELEASE.

### **CHANGED**

- For programmatic usage of the function `manga` in every provider scripts, you can now change whether the function return the chapters and its metadata (which is significantly slower), just the link to the chapters, or none at all.
Ex.:

```python
from mangdl.providers import Provider

prov = Provider("acescans")
print(prov.manga('https://acescans.xyz/manga/hakoniwa-oukoku-no-souzoushu-sama/', chs=0))
```

`chs = 0` means the function will return an empty dictionary; `1`: links to the chapters; `2`: Ch object derived from the chapter's link. If the given integer is not 0-2 (inclusive), it will fallback to `1`.

## **MangDL v.0.0.0-alpha.2**

PROVIDERS SPREE.

### **ADDED**

- <a target="_blank" href="https://acescans.xyz">Ace Scans</a> provider

### **FIXED**

- Flamescans' chapter function throwing an error from untested code

## **MangDL v.0.0.0-alpha.1**

### **ADDED**

-  <a target="_blank" href="https://danke.moe">Danke fürs Lesen</a> provider

## **MangDL v.0.0.0-alpha.0**

START OF SEMANTIC VERSIONING.

### **ADDED**

- <a target="_blank" href="https://hachirumi.com">Hachirumi</a> provider

### **CHANGED**

- An intermediary script between the provider scripts and the cli has been made, which can also be used thru programmatic usage.

Ex.:

```python
from mangdl.providers import Provider
from mangdl.api.base import Search

prov = Provider("mangadex")
for i in prov.search(Search("sachi-iro no one room")):
    print(i)
```

- Removed saving and loading configs

<sub>
    <i>
        <b>NOTE:</b> changes have only been tracked since v.0.0.0-alpha.0
    </i>
</sub>
