<h1 align="center" style="font-weight: bold">
    CHANGELOG
</h1>

## **MangDL v.0.0.0**

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
