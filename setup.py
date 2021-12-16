from setuptools import find_packages, setup

setup(
    name="MangDL",
	author="whinee",
	author_email="whinyaan@gmail.com",
    version="0.0.1",
    description="The most inefficent Manga downloader for PC",
    url="https://github.com/MangDL/MangDL",
	license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	packages=find_packages(),
	include_package_data=True,
    python_requires=">=3.9",
	install_requires=[
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
