from setuptools import find_packages, setup

setup(
    name="mangdl",
	author="whitespace-negative",
	author_email="whinyaan@gmai.com",
    version="0.0.1",
    description="Store files in Discord.",
    url="https://github.com/whitespace-negative/manga-dl",
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
		"click",
		"lxml",
        "patool",
        "pyyaml",
        "tabulate",
        "toml",
        "tqdm",
        "yachalk"
	],
	entry_points = {
        'console_scripts': ['mangdl=mangdl.cli:cli'],
    },
)
