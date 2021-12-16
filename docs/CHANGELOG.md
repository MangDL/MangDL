<h1 align="center" style="font-weight: bold">
    CHANGELOG
</h1>

**MangDL v.0.0.0-alpha.0**

START OF SEMANTIC VERSIONING.

**ADDED**
- Hachirumi provider

**CHANGED**
- An intermediary script between the provider scripts and the cli has been made, which can also be used thru programmatic usage.
Ex.:
```python
from mangdl import Provider
from mangdl.API.Base import Search

md = Provider("mangadex")
for i in md.search(Search("sachi-iro no one room")):
    print(i)
```

**REMOVED**
- Saving and loading configs

<sub>
    <i>
        <b>NOTE:</b> changes have only been tracked since v.0.0.0-alpha.0
    </i>
</sub>
