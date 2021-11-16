URLS=[
"mangdl/index.html",
"mangdl/cli.html",
"mangdl/API/index.html",
"mangdl/API/Base.html",
"mangdl/API/Providers/index.html",
"mangdl/API/Providers/manganato.html",
"mangdl/API/Providers/flamescans.html",
"mangdl/API/Providers/catmanga.html",
"mangdl/API/Providers/mangadex.html",
"mangdl/utils/index.html",
"mangdl/utils/log.html",
"mangdl/utils/style.html",
"mangdl/utils/settings.html",
"mangdl/utils/exceptions.html",
"mangdl/utils/globals.html",
"mangdl/utils/utils.html"
];
INDEX=[
{
"ref":"mangdl",
"url":0,
"doc":""
},
{
"ref":"mangdl.cli",
"url":1,
"doc":""
},
{
"ref":"mangdl.API",
"url":2,
"doc":""
},
{
"ref":"mangdl.API.Base",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.req",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.req.get",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.req.options",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.req.head",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.req.post",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.req.put",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.req.patch",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.req.delete",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.soup",
"url":3,
"doc":"Returns a soup from the given url. Args: url (str): URL to get the soup from. Returns: BeautifulSoup: the soup",
"func":1
},
{
"ref":"mangdl.API.Base.Vls",
"url":3,
"doc":"Vls(vdict: Dict[str, Any], ls: List[str])"
},
{
"ref":"mangdl.API.Base.Vls.vdict",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Vls.ls",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Search",
"url":3,
"doc":"Search(title: str, lang: List[str] =  , excludelang: List[str] =  , demo: List[str] =  , contentrating: List[str] =  , status: List[str] =  , order: str =  , authors: List[str] =  , artists: List[str] =  , year: int = None, includetags: List[str] =  , includemode: str = None, excludetags: List[str] =  , excludemode: str = None, range: Callable Union[int, float , bool] =  at 0x7f0f309044c0>, cover: bool = False, directory: str = None, overwrite: bool = False, retry: int = 3, retryprompt: bool = False, threads: int = 5, verbosity: int = 4, saveconfig: str = None, loadconfig: str = None, overridelc: bool = False)"
},
{
"ref":"mangdl.API.Base.Search.title",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Search.lang",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Search.excludelang",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Search.demo",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Search.contentrating",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Search.status",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Search.order",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Search.authors",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Search.artists",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Search.includetags",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Search.excludetags",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Search.year",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Search.includemode",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Search.excludemode",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Search.range",
"url":3,
"doc":"",
"func":1
},
{
"ref":"mangdl.API.Base.Search.cover",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Search.directory",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Search.overwrite",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Search.retry",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Search.retryprompt",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Search.threads",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Search.verbosity",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Search.saveconfig",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Search.loadconfig",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Search.overridelc",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Ch",
"url":3,
"doc":"Use the template below: Ch( url = ch = vol = title = views = uploaded_at = scanlator_groups = user = imgs = )"
},
{
"ref":"mangdl.API.Base.Ch.url",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Ch.ch",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Ch.vol",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Ch.title",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Ch.scanlator_groups",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Ch.imgs",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Ch.views",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Ch.uploaded_at",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Ch.user",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Manga",
"url":3,
"doc":"Use the template below: Manga( url = , title = , author = , covers = , alt_titles = , status = , demographics = , content_rating = , genres = , updated_at = , created_at = , views = , description = , links = , chapters = , )"
},
{
"ref":"mangdl.API.Base.Manga.url",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Manga.title",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Manga.author",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Manga.covers",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Manga.alt_titles",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Manga.genres",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Manga.links",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Manga.chapters",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Manga.status",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Manga.demographics",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Manga.content_rating",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Manga.updated_at",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Manga.created_at",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Manga.views",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Manga.description",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.tblp",
"url":3,
"doc":"Table prompt. Receive a list of manga title, format it in a table form and print, then prompt the user to choose from the list using an index. Args: ls (List[str]): List of manga title. Returns: click.prompt: The user prompt to choose the manga.",
"func":1
},
{
"ref":"mangdl.API.Base.sanitize_filename",
"url":3,
"doc":"Sanitize the given filename. Args: filename (str): The filename to be sanitized. Returns: str: Sanitized filename.",
"func":1
},
{
"ref":"mangdl.API.Base.get_extension",
"url":3,
"doc":"Get the file extension of a file from the given filename. Args: filename (str): The filename to get the file extension from. Returns: str: The file extension from the given filename.",
"func":1
},
{
"ref":"mangdl.API.Base.ordinal",
"url":3,
"doc":"Convert the given number to ordinal number. Args: n (int): The number to convert into ordinal number. Returns: str: The said ordinal number.",
"func":1
},
{
"ref":"mangdl.API.Base.cr",
"url":3,
"doc":"Returns a function that checks if the given int is within the range or not. The range is calculated from the given string. Args: rs (str): The range string where the range is calculated from. Returns: Callable int], bool]: The function that checks if the given int is within the range or not.",
"func":1
},
{
"ref":"mangdl.API.Base.Downloader",
"url":3,
"doc":""
},
{
"ref":"mangdl.API.Base.Downloader.dlf",
"url":3,
"doc":"Individual image downloader. Args: file (str): List containing the filename and the url of the file.",
"func":1
},
{
"ref":"mangdl.API.Base.Downloader.dlch",
"url":3,
"doc":"Individual chapter downloader. Args: k (Union[int, float]): Chapter number. v (List[str]): List of image urls.",
"func":1
},
{
"ref":"mangdl.API.Base.Downloader.dl",
"url":3,
"doc":"",
"func":1
},
{
"ref":"mangdl.API.Base.Downloader.dl_chdls",
"url":3,
"doc":"",
"func":1
},
{
"ref":"mangdl.API.Base.Downloader.cli",
"url":3,
"doc":"",
"func":1
},
{
"ref":"mangdl.API.Providers",
"url":4,
"doc":""
},
{
"ref":"mangdl.API.Providers.manganato",
"url":5,
"doc":""
},
{
"ref":"mangdl.API.Providers.manganato.manga",
"url":5,
"doc":"",
"func":1
},
{
"ref":"mangdl.API.Providers.manganato.chapter",
"url":5,
"doc":"",
"func":1
},
{
"ref":"mangdl.API.Providers.manganato.search",
"url":5,
"doc":"",
"func":1
},
{
"ref":"mangdl.API.Providers.manganato.cli_search",
"url":5,
"doc":"",
"func":1
},
{
"ref":"mangdl.API.Providers.manganato.dl",
"url":5,
"doc":"",
"func":1
},
{
"ref":"mangdl.API.Providers.manganato.cli_dl",
"url":5,
"doc":"",
"func":1
},
{
"ref":"mangdl.API.Providers.flamescans",
"url":6,
"doc":""
},
{
"ref":"mangdl.API.Providers.flamescans.manga",
"url":6,
"doc":"Returns a Manga object from the given url. Args: url (str): url of the manga Returns: Manga",
"func":1
},
{
"ref":"mangdl.API.Providers.flamescans.chapter",
"url":6,
"doc":"Return a Ch object from the given url. Args: url (str): url of the chapter Returns: Ch",
"func":1
},
{
"ref":"mangdl.API.Providers.flamescans.dl_search",
"url":6,
"doc":"Used for downloading when imported. Args: s (Search): [description] Returns: Dict[str, str]: [description]",
"func":1
},
{
"ref":"mangdl.API.Providers.flamescans.search",
"url":6,
"doc":"Can be used for searching manga when using this project as a module. Args: s (Search): Search dataclass, search parameters for searching. Returns: List[Manga]: Search results.",
"func":1
},
{
"ref":"mangdl.API.Providers.flamescans.cli_search",
"url":6,
"doc":"Format click arguments and options to their respective types, then pass that to  dl_search for it to return the search results. Args: title (str): Title of the manga to search for. Returns: Dict[str, str]: Search results",
"func":1
},
{
"ref":"mangdl.API.Providers.flamescans.cli_dl",
"url":6,
"doc":"Used for downloading when using cli. Args: title (str): Title of the manga to download.",
"func":1
},
{
"ref":"mangdl.API.Providers.catmanga",
"url":7,
"doc":""
},
{
"ref":"mangdl.API.Providers.catmanga.manga",
"url":7,
"doc":"Returns a Manga object from the given url. Args: url (str): url of the manga Returns: Manga",
"func":1
},
{
"ref":"mangdl.API.Providers.catmanga.chapter",
"url":7,
"doc":"Return a Ch object from the given url. Args: url (str): url of the chapter Returns: Ch",
"func":1
},
{
"ref":"mangdl.API.Providers.catmanga.squery",
"url":7,
"doc":"Custom search query. Args: query (str): String to search for in the . possibilities (List[str]): [description] cutoff (int, optional): [description]. Defaults to 0.6. processor (Callable Any], Any], optional): [description]. Defaults to lambdar:r. Yields: [type]: [description]",
"func":1
},
{
"ref":"mangdl.API.Providers.catmanga.search",
"url":7,
"doc":"Can be used for searching manga when using this project as a module. Args: s (Search): Search dataclass, search parameters for searching. Returns: List[Manga]: Search results.",
"func":1
},
{
"ref":"mangdl.API.Providers.catmanga.dl_search",
"url":7,
"doc":"Used for downloading when imported. Args: s (Search): [description] Returns: Dict[str, str]: [description]",
"func":1
},
{
"ref":"mangdl.API.Providers.catmanga.cli_search",
"url":7,
"doc":"Format click arguments and options to their respective types, then pass that to  dl_search for it to return the search results. Args: title (str): Title of the manga to search for. Returns: Dict[str, str]: Search results",
"func":1
},
{
"ref":"mangdl.API.Providers.catmanga.dl",
"url":7,
"doc":"Used for downloading when using the project as a module. Args: url (str): URL of the manga to download.",
"func":1
},
{
"ref":"mangdl.API.Providers.catmanga.cli_dl",
"url":7,
"doc":"Used for downloading when using cli. Args: title (str): Title of the manga to download.",
"func":1
},
{
"ref":"mangdl.API.Providers.mangadex",
"url":8,
"doc":""
},
{
"ref":"mangdl.API.Providers.mangadex.ra",
"url":8,
"doc":"Return the current time subracted to retry after header from the given response object. Args: resp (httpx.Response): Response object to get the retry after header from. Returns: int: current time subracted to retry after header.",
"func":1
},
{
"ref":"mangdl.API.Providers.mangadex.value",
"url":8,
"doc":"Returns the first value of the first key from a dictionary Args: d (dict[Any, Any]): Dictionary to get the first value from. Returns: Any: First value of the given dictionary.",
"func":1
},
{
"ref":"mangdl.API.Providers.mangadex.paginate",
"url":8,
"doc":"Paginate results from an API endpoint with limited results per calls. Args: log (Callable str, str, str], None]): logger url (str): url of the endpoint limit (int, optional): items per page. Defaults to 100. params (dict[Any, Any], optional): parameters for the request. Defaults to {}. Returns: list[dict[str, Any : paginated results",
"func":1
},
{
"ref":"mangdl.API.Providers.mangadex.manga",
"url":8,
"doc":"Returns a Manga object from the given url. Args: url (str): url of the manga Returns: Manga",
"func":1
},
{
"ref":"mangdl.API.Providers.mangadex.chapter",
"url":8,
"doc":"Return a Ch object from the given url. Args: url (str): url of the chapter Returns: Ch",
"func":1
},
{
"ref":"mangdl.API.Providers.mangadex.dl_search",
"url":8,
"doc":"Used for downloading when imported. Args: s (Search): [description] Returns: Dict[str, str]: [description]",
"func":1
},
{
"ref":"mangdl.API.Providers.mangadex.search",
"url":8,
"doc":"Can be used for searching manga when using this project as a module. Args: s (Search): Search dataclass, search parameters for searching. Returns: List[Manga]: Search results.",
"func":1
},
{
"ref":"mangdl.API.Providers.mangadex.cli_search",
"url":8,
"doc":"Format click arguments and options to their respective types, then pass that to  dl_search for it to return the search results. Args: title (str): Title of the manga to search for. Returns: Dict[str, str]: Search results",
"func":1
},
{
"ref":"mangdl.API.Providers.mangadex.dl",
"url":8,
"doc":"Used for downloading when using the project as a module. Args: url (str): URL of the manga to download.",
"func":1
},
{
"ref":"mangdl.API.Providers.mangadex.cli_dl",
"url":8,
"doc":"Used for downloading when using cli. Args: title (str): Title of the manga to download.",
"func":1
},
{
"ref":"mangdl.utils",
"url":9,
"doc":""
},
{
"ref":"mangdl.utils.log",
"url":10,
"doc":""
},
{
"ref":"mangdl.utils.log.logger",
"url":10,
"doc":"Colorful logger? Args: td (datetime.now): epoch of the logger l (str): level of the message to be logged"
},
{
"ref":"mangdl.utils.log.logger.log",
"url":10,
"doc":"The logger itself. Args: msg (str): message to be logged name (str, optional): name of the log. Defaults to None.",
"func":1
},
{
"ref":"mangdl.utils.style",
"url":11,
"doc":""
},
{
"ref":"mangdl.utils.settings",
"url":12,
"doc":""
},
{
"ref":"mangdl.utils.settings.readcfg",
"url":12,
"doc":"Read the contents of a file with the given file name. Args: file (str): File name of the file to read the contents of. Returns: Any: The contents of the file.",
"func":1
},
{
"ref":"mangdl.utils.settings.stg",
"url":12,
"doc":"Retrieve dictionary value of the config file with the given file name using recursive indexing with a string. ex.: Given that settings.json contains:  {\"data\": {\"attr\": {\"ch\": 1 }  stg(\"data/attr/ch\", \"settings.json\") will return  1 Args: stg (str): Directory of the value to be retrieved. file (str, optional): File name of the file to get the value from. Defaults to  path.join(dn(ap(__file__ , \"settings.json\") . Returns: Any: The retrieved value.",
"func":1
},
{
"ref":"mangdl.utils.settings.wr_stg",
"url":12,
"doc":"Rewrite dictionary value of the config file with the given file name using recursive indexing with a string. ex.: Given that settings.json contains:  {\"data\": {\"attr\": {\"ch\": 1 }  wr_stg(\"data/attr/ch\", 2) will rewrite settings.json to be:  {\"data\": {\"attr\": {\"ch\": 2 } Args: stg (str): Directory of the value to be rewrited. value (Any): Value to rewrite to. file (str, optional): File name of the file to rewrite the value from. Defaults to path.join(dn(ap(__file__ , \"settings.json\"). Raises: FileNotFoundError: Raised if the file is not found.",
"func":1
},
{
"ref":"mangdl.utils.exceptions",
"url":13,
"doc":""
},
{
"ref":"mangdl.utils.exceptions.UnexpectedDatetimeFormat",
"url":13,
"doc":"Common base class for all non-exit exceptions."
},
{
"ref":"mangdl.utils.globals",
"url":14,
"doc":""
},
{
"ref":"mangdl.utils.utils",
"url":15,
"doc":""
},
{
"ref":"mangdl.utils.utils.dnrp",
"url":15,
"doc":"Get the directory component of a pathname by n times recursively then return it. Args: file (str): File to get the directory of. n (int, optional): Number of times to get up the directory  Defaults to 1. Returns: op (str): The directory component got recursively by n times from the given pathname",
"func":1
},
{
"ref":"mangdl.utils.utils.de",
"url":15,
"doc":"Defaults. Return a if a is True, else returns d. Args: a (Any): Object to be tested, will be returned if evaluates to True. d (Any): Default object to be returned if  a evaluates to False. Returns: Any",
"func":1
},
{
"ref":"mangdl.utils.utils.dd",
"url":15,
"doc":"Defaults dictionary. Overwrite the items in the default dict with the items in the d dict. Args: default (Dict[Any, Any]): The dict to rewrite the items to. d (Union[Dict[Any, Any], None]): The dict to rewrite the items from. Returns: dict[Any, Any]",
"func":1
},
{
"ref":"mangdl.utils.utils.ddir",
"url":15,
"doc":"Retrieve dictionary value using recursive indexing with a string. ex.:  ddir({\"data\": {\"attr\": {\"ch\": 1 }, \"data/attr/ch\") will return  1 Args: dict (dict): Dictionary to retrieve the value from. dir (str): Directory of the value to be retrieved. Returns: op (Any): Retrieved value.",
"func":1
},
{
"ref":"mangdl.utils.utils.dt",
"url":15,
"doc":"Remove timezone from datetime. Arguments: dt {str}  datetime ? Raises: exceptions.UnexpectedDatetimeFormat: raised when the given string is not a datetime formatted at the following format:  Returns: str  [description]",
"func":1
},
{
"ref":"mangdl.utils.utils.cao",
"url":15,
"doc":"Retruns wrappers for a click command evaluated from the given arguments. Args: group (click.group): Command group of the command to be under. cmd (str): Name of the command. Returns: List[Callable Callable Any], Any , Callable Any], Any ]: The wrappers.",
"func":1
},
{
"ref":"mangdl.utils.utils.command",
"url":15,
"doc":"Wrapper for click commands. Args: group (click.group): Command group of the command to be under. Returns: Callable Callable Any], Any , Callable Any], Any ",
"func":1
},
{
"ref":"mangdl.utils.utils.parse_list",
"url":15,
"doc":"Takes a string and evaluates it to a list if it is a list, else it splits it into a list. It then evaluates the values of that list. Args: opt (Union[str, None]): The object to be evaluated.",
"func":1
}
]