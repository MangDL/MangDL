from setuptools import find_packages, setup

with open("version", "r") as f:
    version = f.read().strip()
with open("docs/README.md", "r", encoding="utf-8") as f:
    ld = f.read()

setup(
    name="MangDL",
	author="whinee",
	author_email="whinyaan@gmail.com",
    version=version,
    description="The most inefficent Manga downloader for PC",
    long_description=ld,
    long_description_content_type="text/markdown",
    url="https://github.com/MangDL/MangDL",
    project_urls={
        'Documentation': 'http://mangdl.rf.gd/docs',
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
