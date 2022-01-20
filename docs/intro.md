<h1 align="center" style="font-weight: bold">
    PROGRAMMATIC USAGE
</h1>

MangDL is a manga downloader that can also give the metadata of a manga and chapter. Where you can buy it on Amazon, when it was last updated, you name it. That's it. That's what sets it apart from others, a shitty feature nobody asked for.

## **Start**

First, we choose our provider from [this link](https://mdl.pages.dev/providers). We then initialize a new provider.

```python
>>> from mangdl.providers import Provider
>>> prov = Provider("mangadex")
```

## **Manga**

Now, to get the manga's metadata, call the provider's manga function and pass the url.

```python
>>> manga = prov.manga("https://mangadex.org/title/010a8606-ab4f-4e3e-82ce-17f19b02f262")
>>> manga.url
'https://mangadex.org/title/010a8606-ab4f-4e3e-82ce-17f19b02f262/happy-sugar-life'
>>> manga.title
Happy Sugar Life
>>> manga.author
['Kagisora Tomiyaki']
>>> manga.artist
['Kagisora Tomiyaki']
>>> manga.cover
[
    'https://uploads.mangadex.org/covers/010...bf8.jpg',
    ...,
    'https://uploads.mangadex.org/covers/010...72c.jpg'
]
>>> manga.alt_titles
['White Sugar Garden, Black Salt Cage', ..., 'Сладкая жизнь']
>>> manga.updated_at
'2021-11-23T21:12:00+00:00'
>>> manga.created_at
'2018-12-07T02:17:58+00:00'
>>> manga.views
None
>>> manga.chapters
{}
>>> manga.description
'High-schooler Matsuzaka Satou has a reputation for being easy, but ... as an extra.'
>>> manga.links
{
    'al': 'https://anilist.co/manga/86655',
    ...,
    'engtl': 'https://yenpress.com/9781975303303/happy-sugar-life-vol-1/'
}
```

To get the chapter links, set the keyword argument `ch` to 1.

```python
>>> manga = prov.manga("https://mangadex.org/title/010a8606-ab4f-4e3e-82ce-17f19b02f262", chs=1)
>>> manga.chapters
{
    48.5: 'https://mangadex.org/chapter/3b1a2269-1b85-401d-8b7c-d09d005d7517',
    48.4: 'https://mangadex.org/chapter/e6017ae9-7637-47fb-af1c-cb1cf403a6ee',
    48.3: 'https://mangadex.org/chapter/ba690c42-4e2b-4387-ade4-247c3e1cfa43',
    ...,
    1: 'https://mangadex.org/chapter/d0c72cb4-e0d2-4131-9eed-9858610c2a2d'
}
```

To get the chapter full metadata, set the keyword argument `ch` to 2.

```python
>>> manga = prov.manga("https://mangadex.org/title/010a8606-ab4f-4e3e-82ce-17f19b02f262", chs=2)
>>> manga.chapters
{
    48.5: Ch(
        url='https://mangadex.org/chapter/3b1a2269-1b85-401d-8b7c-d09d005d7517',
        ch=48.5,
        vol={},
        title='Sato',
        views=0,
        uploaded_at='2020-07-10T18:00:06+00:00',
        scanlator_groups=[],
        user=None,
        imgs=[
            'https://uploads.mangadex.org/data/a65...38c.jpg',
            ...,
            'https://uploads.mangadex.org/data/a65...768.png'
        ]
    ),
    ...,
    1: Ch(
        url='https://mangadex.org/chapter/d0c72cb4-e0d2-4131-9eed-9858610c2a2d',
        ch=1,
        vol=1,
        title='The Sugar Girl Eats Love',
        views=0,
        uploaded_at='2018-02-03T14:38:20+00:00',
        scanlator_groups=[],
        user=None,
        imgs=[
            'https://uploads.mangadex.org/data/8d3...04e.jpg',
            ...,
            'https://uploads.mangadex.org/data/8d3...c15.png'
        ]
    )
}
```

## **Chapter**

To get the chapter's metadata, call the provider's chapter function and pass the chapter's URL to it.

```python
>>> chapter = prov.chapter("https://mangadex.org/chapter/a5dd4835-c1f3-446d-89b7-3f6b5e115fa5")
>>> chapter.url
'https://mangadex.org/chapter/a5dd4835-c1f3-446d-89b7-3f6b5e115fa5'
>>> chapter.ch
19.5
>>> chapter.vol
5
>>> chapter.title
'Interlude'
>>> chapter.views
0
>>> chapter.uploaded_at
'2018-02-03T14:47:25+00:00'
>>> chapter.scanlator_groups
[]
>>> chapter.user
None
>>> chapter.imgs
[
    'https://uploads.mangadex.org/data/834...12c.jpg',
    ...,
    'https://uploads.mangadex.org/data/834...44f.png'
]
```
