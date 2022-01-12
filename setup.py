from setuptools import find_packages, setup
setup(
    name="MangDL",
    author="whinee",
    author_email="whinyaan@gmail.com",
    version='3.0.1.0',
    description="The most inefficent Manga downloader for PC",
    long_description='''<!-- Repository Name. Preferrably 1-5 words long. -->
<p align="center">
    <img src="./assets/images/icons/logo-white.png" id="logo" width="300rem" height="auto" style="display: block; margin: auto;">
</p>

<h1 align="center" style="font-weight: bold">
    <span id="min-block-shrink">▀▄▀▄▀▄</span>
    <span id="min-block">MangDL</span>
    <span id="min-block-shrink">▀▄▀▄▀▄</span>
</h1>

<!-- Description. Preferrably 1 sentence long. -->
<h3 align="center" style="font-weight: bold">
    Manga Downloader
</h3>

<p align="center">
    <a href="https://github.com/MangDL/MangDL/issues">
        <img src="https://img.shields.io/github/issues/MangDL/MangDL.svg?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAABmJLR0QA/wD/AP+gvaeTAAACVUlEQVR4nO3doW5UQRTG8XPaEHwLBgQhCGoQJLwAiiYY3qCG10DgCc/QJ0AgMCTUIkCCqiAhkCBQpNAW0g+xS5pguLv3DPeb3f/P35OZ+XJm7+yIGwEAAAAAALAQSW813pup5zHExtQDGOi0oMZJQY3megmkYjEJpBCBmCEQMwRihkDMVCzmcUGN5tYpEDqkEOcQM3SIGQIxQyBmCMQMgZghEDMVr70cDAvRIWYIxAyBmCEQMwRihkDMEIgZLqjMcB9ihi3LDIGYIRAzYxfzLDN/loyksS4CyczTiNCIEhUvBf9FF4HMjVnULl55I/oKZMy21cXvRwSB2OkpkDFbFoE0QIeYIRAzBGKGQMyMWVTOIQ3QIWYIxAyBmOFgaIYOMUMgZgjEDIGY4WBohg4xw2uvGTrEzFoEklMPYChJ1yPizpKPv87Mj5XjAQAAAACgiW5O6n+bn9zvRsStiNiK2Vy+RsT7iDjIzMMJh7c+JN2W9ELS2T++F/JS0rJ/tWAISXuSjhf4iMuJpIdTj3slSdqV9Gvh7+rMnrk/9fhXiqQLkg6XCOOPD5IuTj2PIXq5D3kQETdGPH9tXsNeL4HsFtS4V1CjuV4C2SmocbOgRnO9BLJVUONSQY3megnkqKDGt4IazfUSyCeTGs31EsirghoHBTUQESHpiqTvI84hPyRdnXoeQ3TRIZn5OSKejCjxNDO72LK6IWlT0rMluuO5pM2px7+SJG1IeiTpaOA29bi3MLq8D5F0OSL24vw+ZDvO70PexewHfD8zv0w2SAAAAAAAsAJ+A9PfbN9hclgfAAAAAElFTkSuQmCC">
    </a>
    <a href="https://github.com/MangDL/MangDL/network/members">
        <img src="https://img.shields.io/github/forks/MangDL/MangDL.svg?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAABmJLR0QA/wD/AP+gvaeTAAAFKElEQVR4nO2dS4gcRRjH/xXdoKiIaESNio8YCbKKRgSJ4knEg8km0eArQUTwZIJXL8GTWYMoehC8xgfRgxvjUfAg+IoPsi5Bze76TiIo4jqCu5vMz0NNS+zMzM5OV+9X3VM/GHabXb761/zpenzdVSUlEolEIpFIJMLjyggKLJc00vrcJOnS1p9+lvSFpDFJY865uTLKT5wEsAmYYmEmgY3WemsLsAx4tgcj8owCy6z11w5gdx9mZOyy1l8r8M1UUUas61ELgOX4/qAoU/jBwEATou0ekXR1gDhXSVofIE6lCWFIyJHSwDdbIQxZGyBGxs0BY1WSEIZcHCBGxsqAsSrJ6QFilDLbt4QqZxrobVbeK4cjqE+1Mw3AawEN2WNYj3pkGoD7AxqyxbAe/ZiRMWql+xSAIeD7AGZMAyH6tH7qUK9MA7A+QIU2GWmvZ6YBeL5AZZ4z1L0lgBkZ91rV4xQAB7zQjxmA2dAZeD2gIa9a1aMj+Pb4ux7ETxNBuwt8E9CQr63r0xZ8R/8gsLeN6L3AA8CQtU5JAmYCGjJTVE/pTQXA/wp0LqqZPdCQdFagcA3n3DlFAsQzobHjWEyxkiHSpwFjfVw0QDJEeidgrP1FA6Q+xA8uJiVdXjDUtKRrnXPHiwQZ+DvEOTcv6YkAoXYUNWNJyI8LrfV0gv4mtRm7rfX3TIUMccCLizSiic8SR9UMd6UqhmTgc1s/9GDGJHCPtd5FUzVDpP8ywFuBsZz8efwDufswelRQmCoakgGsyt8VZZc58KOsBbgsd/1L2QUmQ7qTfyPzaNkFJkO6c0vuerzsApMh3bk9dx0y72VDVTt1YDgnfQ44t+xy0x3SmUdz1+855/40URKSKt4hwIXA3znp26x1BaGihuTfxjwKnGmtKwhVMwQ/Q8/zpLWuYFTJEOAuYDYneQI4w1pbMKpiCPBYGzPmgJALkuyJ3RDgIuCtNs1UE9hqrS84sRoCrMQvJWi0MeMEsN1aYynEZAiwAngEn1afb2ME+OHuZkudpWJpCHA+cDewE/gAON7BhIwPgdVLqTFPNR+y5MCvYLpS0vWSrpM0LOlGSdf0GOJHSTsl7XHOnShFZI9UzhDgPPkvfrj18wZ5E/p5HfSApJckvemcmw0msgDRGwKskXSHpNskrZN0RYFwTUkfya+ifds5N1VcYViiNAS4VdJmSRskrSoQalbSl/KveH4i6X3n3K/FFZZHNIYAZ0vaJulx+aZosRyT9JWkidZnXNJ4lGvJu2BuCHCafKr7afW2K8SspIPyC/jHJR2SNOGc+700kXWi27AXWAMcXGAo2gDeBbYDa4lkoU9l6WQI8BDwVwcT/gHeAO4kppWtdaCdIcCODkbMAE8BK6x115Y2X/rD+FxRnv1A0SUBiYVo88Xnc0gNjDYNGEg6NE0nm7HOWuNA0cWMJhGsUx84uhjysrW2gaSDGX8AF1hrixGrF+Vecc79ZlT2YNPhDun1OUUiNG3MOGStKWaWIrm4WtKR1u+XLEF5iUQikVga0hlUdYeq7wxdF6jLztB1gXQGVTxQt52hqwx13RnaiHQGVWSkM6giI51BFRnpDKrIiG3837QWYE0IQ44s/C8msSpJCEM+CxAj40DAWJUkhCH7AsTICLnL9GCCP5ricJoYRgSwsaAZTWDgJ4VBodixc89Y668d+PT7aB93xi5S+r08gBF661O+BTZY642Nsh7hDsmvoB2RT61kj3B/kvS5/MhsX+tkgkQikUgkEolEomT+BQYopfF8o1GKAAAAAElFTkSuQmCC">
    </a>
    <a href="https://github.com/MangDL/MangDL/stargazers">
        <img src="https://img.shields.io/github/stars/MangDL/MangDL.svg?style=flat-square&logo=data:image/png;base64,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">
    </a>
    <a href="https://github.com/MangDL/MangDL/graphs/contributors">
        <img src="https://img.shields.io/github/contributors/MangDL/MangDL.svg?style=flat-square&logo=data:image/png;base64,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">
    </a>
    <a href="https://mdl.pages.dev/license.html">
        <img src="https://img.shields.io/badge/LICENSE-A31F34?style=flat-square&logoWidth=25&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAANwAAAByCAYAAAA4TL8fAAADvElEQVR4nO3bsYkdVxiG4c2EA6kCY5WgAt2AMuVbgntRC+rgcoeFTRbDcQ3/OxwxjJ8P/vTwBvOE8/J8PteuO47j35cTO47jubNvrfX5RNuvzW1/nWj7ubPt4+PjW21ba33Z2Xb1e9n5OHCn2oC74QHX24ALA27j48CdagPuhgdcbwMuDLiNjwN3qg24Gx5wvQ24MOA2Pg7cqTbgbnjA9TbgwoDb+Dhwp9qAu+EB19uACwNu4+PAnWoD7oYHXG8DLgy4jY8Dd6oNuBsecL0NuDDgNj4O3Kk24G54wPU24MKA2/g4cKfagLvhAdfbgAsDbuPjwJ1qA+6GB1xvAy4MuI2PA3eqDbgbHnC97bLg3t7evr+/v/+z69ZaX2vbWuuPnW1XP+B622XB2YUHXG4DzuYDLrcBZ/MBl9uAs/mAy23A2XzA5TbgbD7gchtwNh9wuQ04mw+43AaczQdcbgPO5gMutwFn8wGX24Cz+YDLbcDZfMDltsuCW2v9vdZ63Xh/nmj7dBzH6657PB4/attvGXC57crgfq69O/M/3OfN39yztv2WAZfbgGttwAGX2oBrbcABl9qAa23AAZfagGttwAGX2oBrbcABl9qAa23AAZfagGttwAGX2oBrbcABl9qAa23AAZfagGttwAGX2oBrbcABl9qAa23AAZfagGttwAGX2oBrbcABl9qAa23AAZfagGttwAGX2oBrbcABl9qAa23AAZfagGttwAGX2oBrbcABl9qAa23AAZfagGttwAGX2oBrbcABl9qAa23AAZfagGttwAGX2oBrbcABl9qAa23AAZfagGttwAGX2oBrbcABl9qAa23AAZfagGttwAGX2oBrbcABl9qAa23AAZfagGttwAGX2oBrbcABl9qAa23AAZfagGttwAGX2oBrbcABl9qAa23AXRXc4/H4cRzH665ba32qbcDlNuCuCu7KAy63AQfcfMDlNuCAmw+43AYccPMBl9uAA24+4HIbcMDNB1xuAw64+YDLbcABNx9wuQ044OYDLrcBB9x8wOU24ICbD7jcBhxw8wGX24ADbj7gchtwwM0HXG4DDrj5gMttwAE3H3C5DTjg5gMutwEH3HzA5TbggJsPuNwGHHDzAZfbgANuPuByG3DAzQdcbgMOuPmAy23AATcfcLkNOODmAy63AQfcfMDlNuCAmw+43AYccPMBl9uAA24+4HIbcMDNB1xuAw64+YDLbcABNx9wuQ044OYDLrcBB9x8wOU24ICbD7jcBhxw8wGX2/7X4P4DxDPxnlw4RDoAAAAASUVORK5CYII=">
    </a>
</p>
<p align="center">
    <a href="https://app.codacy.com/gh/MangDL/MangDL/dashboard?branch=master">
        <img alt="Codacy Badge" src="https://img.shields.io/codacy/grade/93418e488727439bb71f3f779860ced2/?style=flat-square">
    </a>
    <a href="https://github.com/MangDL/MangDL/releases">
        <img alt="GitHub release (latest by date including pre-releases)" src="https://img.shields.io/github/v/release/MangDL/MangDL?include_prereleases&style=flat-square">
    </a>
    <a href="https://github.com/MangDL/MangDL/releases">
        <img alt="GitHub Workflow Status" src="https://img.shields.io/github/workflow/status/MangDL/MangDL/Build?label=Build&style=flat-square">
    </a>
</p>
<p align="center">
    <a target="_blank" href="https://discord.com/invite/JbAtUxGcJZ">
        <img src="https://img.shields.io/discord/889508240495366184.svg?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAQAAADa613fAAAAAmJLR0QA/4ePzL8AAAAJcEhZcwAACxMAAAsTAQCanBgAAAAHdElNRQflCwsPNhJbdTGBAAABx0lEQVR42u1byw7DIAxbUP//l7fDVGktFPIwFDr7vDzcOElF2etFEARBEARBEP8CiZm/35lD6W0JJpInYkkoZl3ChqSAwNe7nY6gKfilFauOoEhIB5Fa/MqIjhgRAd6Y2g6y2bbJiI/G2XFkAOh8taiIncbRJWqGtb3WqUiEBnoQt3zXqBiJ7K567pLrGDUiydPkI1aiNa7ctcExg0FBZEYaNSrpKa/xjyEiawnrWlzPrsjM9biqCZt9AWnNLqyyuCit6aW1grBK4qK0JpfWKsLKxUVpkciIHvF2iOdkBXEa8+sjoZtOecDpsOksrTwJxfGmw6YzkXICjTNBh81/Tq2VlmGeMfcIiZCIksh6rQ6tSJl+/aF4bNq+wtLKE2in5LEZ0CPHJHQpeWyUb7+r9sj+asPxSyIkQiIPJSKCutBkGa36mMnm+I4NocNmdz5idQbuNLbT63kvyB9n/7XxFaU3Gbv/jIj3Et+4i2d1K2dS468CtiwDCUnwizDWPvwNETeSbZHPcUHf2SN0MPG2+3YFdsekGXY4ovaCKLrImO5wX5fVhUFULx5j0z6Hu7oG/G+F6yfX798K8/YpQRAEQRAEQRAEMTM+AjWseCjwIcoAAAAASUVORK5CYII=">
    </a>
</p>

<!-- About section. Preferrably 2-5 sentences long. -->
---

<h4 align="center">
The most inefficient manga downloader for PC (and soon, also a reader)
</h4>

---

<div id="quotes">
    <blockquote>
        <p dir="auto"><b>❝<i>...but I don't think you'll write code valuable enough for them</i></b> (Content creators and/or owners) <b><i>to do that</i></b> (file a DMCA strike against MangDL)<b><i>.</i>"</b></p>
        <p dir="auto">- <a href="https://github.com/justfoolingaround">KR</a></p>
    </blockquote>
    <blockquote>
        <p dir="auto"><b>❝<i><del>whi_ne has good organization</del></i></b> [skills] <b><i><del>and bad code</del></i>❞</b></p>
        <p dir="auto">- <a href='https://github.com/ArjixWasTaken'>Arjix</a></p>
    </blockquote>
</div>

Github: [github.com/MangDL/MangDL](https://github.com/MangDL/MangDL)

Website: [mdl.pages.dev](https://mdl.pages.dev)

## **Downloads**

Since people are looking for the download first, here you go:

Follow [this link](https://mdl.pages.dev/installation.html) to install MangDL in your machine.

## **Important**

This project is a work in progress, use at your own risk.

To be updated, be sure to watch this repository and join the [Discord Support Server](https://discord.com/invite/JbAtUxGcJZ) for MangDL.

For the terms of usage and legals, visit [license](license.md) and [terms of usage & disclaimer](tou_disc.md).

## **Features**

- Ad free
- Batch downloading
- 0% tracking and analytics
- Can be used as a library

### Supported OSes

- Windows
- MacOS
- Linux

## **Sites**

For the full list of providers, visit [this link](providers.md).

<!-- TOC section. Update when adding sections and subsections fitted in TOC. -->
## **Table of Contents**

- [**Important**](#important)
- [**Features**](#features)
  - [Supported OSes](#supported-oses)
- [**Sites**](#sites)
  - [Coming soon™](#coming-soon)
- [**Table of Contents**](#table-of-contents)
- [**Usage**](#usage)
- [**Getting Started**](#getting-started)
  - [**Prerequisites**](#prerequisites)
  - [**Setup**](#setup)
- [**Contributions**](#contributions)
- [**Known Issues and Limitations**](#known-issues-and-limitations)
- [**Future of this project**](#future-of-this-project)
- [**License**](#license)
- [**Credits**](#credits)
  - [Thank you](#thank-you)
  - [MIT Logo](#mit-logo)
  - [Icons](#icons)

<!-- Mention examples of application of this repository. -->
## **Usage**

Before using this project, it is recommended to visit [license](license.md) and [terms of usage & disclaimer](tou_disc.md) for the terms of usage, disclaimer, and legals.

```bash
mangdl -h
```

Downloading:

```bash
mangdl dl <title> [OPTIONS]
```

For programmatic use, visit the documentation: [mdl.pages.dev/docs](https://mdl.pages.dev/docs/index.html)

## **Getting Started**

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### **Prerequisites**

The following are the required programs and/or packages to run this project:

- For all operating systems:
    - Python 3.6 and higher
        <details>
        <summary>To check that you have Python 3.6 and higher installed, in your preferred terminal, run the following command:</summary>

        ```bash
        python3 --version
        ```

        </details>

    - pip (Package Installer for Python)
        <details>
        <summary>To check that you have pip installed, in your preferred terminal, run the following command:</summary>

        ```bash
        pip3 --version
        ```

        </details>

    - git
        <details>
        <summary>To check that you have git installed, in your preferred terminal, run the following command:</summary>

        ```bash
        git --version
        ```

        </details>

    ![uni](assets/images/prereq_uni.png)

- For windows:
    - [Chocolatey](https://chocolatey.org)
        <details>
        <summary>To check that you have Chocolatey installed, in your preferred terminal, run the following command:</summary>

        ```bash
        choco --version
        ```

        </details>

    - [7zip](https://7-zip.org)
        <details>
        <summary>To check that you have 7zip installed, in your preferred terminal, run the following command:</summary>

        ```bash
        7z --version
        ```

        </details>

    <details>
    <summary>You should get a similar output like the following image:</summary>
    <img src="assets/images/prereq_1.png" alt="1">
    </details>

- For [macOS](https://www.apple.com/mac/):
    - [Homebrew](https://brew.sh)
        <details>
        <summary>To check that you have Homebrew installed, in your preferred terminal, run the following command:</summary>

        ```bash
        brew --version
        ```

        </details>

    - [p7zip](https://github.com/jinfeihan57/p7zip)
        <details>
        <summary>To check that you have p7zip installed, in your preferred terminal, run the following command:</summary>

        ```bash
        7z --version
        ```

        </details>

    <details>
    <summary>You should get a similar output like the following image:</summary>
    <img src="assets/images/prereq_2.png" alt="2">
    </details>

- For [Linux](https://www.linux.org/)
    - [p7zip](https://github.com/jinfeihan57/p7zip)
        <details>
        <summary>To check that you have p7zip installed, in your preferred terminal, run the following command:</summary>

        ```bash
        7z --version
        ```

        </details>

    <details>
    <summary>You should get a similar output like the following image:</summary>
    <img src="assets/images/prereq_3.png" alt="3">
    </details>

### **Setup**

Follow [this link](https://mdl.pages.dev/installation.html) to install MangDL in your machine.

# TODO

### Main to do

- [ ] Documentation

    - [x] Bare-bones sites

    - [ ] Migrate every .md file to https://mangdl.github.io

- [ ] Library

    - [ ] Manga Update notifier

    - [ ] Backupable library with an option to store an offsite backup in [supabase.io](https://supabase.io)

- [ ] GUI

    - [ ] Reader

- [ ] MAL / Anilist sync

- [ ] Fully opt-in 99% configureable (mostly opinionated) analytics for new and some sampled features

### Side Quests

- [ ] Installation instructions for Android users

- [ ] Package update notifier

- [ ] Saving command options to config file

- [ ] Submission of new color theme for the CLI and possibly for the future GUI

- [ ] Returning/Downloading translated languages using locale of the machine and an option to override it

## **Contributions**

You can contribute by creating a new issue, or by creating pull requests.

At the time of writing, there are no templates for both creating a new issue and pull requests.

The developer notes however that the said template will be created if a trend of users using this project is evident.

For creating a new issue, please make sure that the said issue is not on the list of closed and open issues.

After checking that that is the case, create a new issue.

The title of the issue must summarize its contents.

The body must contain the following:

- a clear description of the bug
- Python version used for running and/or testing the project
- OS name and version

<!-- Mention the issus and limitations of this repository. Preferrably 1-5 sentences long. -->
## **Known Issues and Limitations**

At the time of writing, this project can not be run in Termux due to a fatal error.

Also, something is broken and I don't know what is, 'cause I forgot!

<!-- Mention the plans for the repository. Preferrably 2-5 sentences long. -->
## **Future of this project**

The TODO will be done, except for that, nothing else.

<!-- License section. Leave unchanged except when updating the year, using a different license, or changing the style altogether. -->
## **License**

### <a target="_blank" href="https://choosealicense.com/licenses/mit/">MIT</a>

Copyright for portions of project [MangDL](https://github.com/MangDL/MangDL) are held by [Github Account [justfoolingaround](https://github.com/justfoolingaround) Owner, 2021] as part of project [AnimDL](https://github.com/justfoolingaround/AnimDL).

All other copyright for project [MangDL](https://github.com/MangDL/MangDL) are held by [Github Account [whinee](https://github.com/whinee) Owner, 2021].

Check the [LICENSE](LICENSE.md) for more details.

## **Credits**

### Thank you:

- To [Arjix](https://github.com/ArjixWasTaken), who helped me in implementing majority of the features and de-minifying my code, making it more readable and more efficient at the same time
- To [KR](https://github/com/justfoolingaround), who let me use the KR-naming scheme like "AnimDL" do
- To whi~nyaan, my alter ego, for just existing (and purring, ofc)
- And to everyone who supported me from the very beginning of this humble project to its release!

### MIT Logo

<a target="_blank" href="https://commons.wikimedia.org/wiki/File:MIT_logo.svg">Massachusetts Institute of Technology</a> (vectorized by <a target="_blank" href="https://en.wikipedia.org/wiki/User:Mysid">Mysid</a>, modified by [whinee](https://github.com/whinee)), Public domain, via Wikimedia Commons

### Icons

<a target="_blank" href="https://icons8.com/icon/102502/exclamation-mark">Exclamation Mark</a>, <a target="_blank" href="https://icons8.com/icon/33294/code-fork">Code Fork</a>, <a target="_blank" href="https://icons8.com/icon/85185/star">Star</a>, <a target="_blank" href="https://icons8.com/icon/34095/group">Group</a>, <a target="_blank" href="https://icons8.com/icon/87276/code">Code</a>, and <a href="https://icons8.com/icon/30888/discord">Discord</a> icons by <a target="_blank" href="https://icons8.com">Icons8</a>

<sub>
    <i>
        <b>NOTE:</b> If a reference or source material is not attributed properly or not at all, please kindly message me at Discord: <a target="_blank" href="https://discord.com/users/867696753434951732">whi_ne#5135</a> or create a pull request so I can properly give credit to their respective authors.
    </i>
</sub>
''',
    long_description_content_type="text/markdown",
    url="https://github.com/MangDL/MangDL",
    project_urls={
        'Documentation': 'https://mdl.pages.dev/docs',
        'Source': 'https://github.com/MangDL/MangDL/',
        'Tracker': 'https://github.com/MangDL/MangDL/issues',
    },
    license="MIT",
    keywords='development python windows macos linux cli wordpress metadata scraper downloader zip tar rar manga provider reader cbr cbz cbt 7zip cb7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[
        "arrow",
        "BeautifulSoup4",
        "click",
        "httpx",
        "lxml",
        "patool",
        "pyyaml",
        "rich",
        "tabulate",
        "toml",
        "tqdm",
        "yachalk",
        "yarl",
    ],
    entry_points = {
        'console_scripts': ['mangdl=mangdl.cli:cli'],
    },
)
