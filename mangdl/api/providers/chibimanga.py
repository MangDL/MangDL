from ..base import soup

scanlator = "Chibimanga"
base_url = "https://www.cmreader.info"
template = "wordpress"

ch_num_fn = "wmcc"
src = "data-src"

def manga_id_fn(soup):
    return soup.select_one("#manga-chapters-holder")["data-id"]

def rch_fn(url):
    data = {"action": "manga_get_chapters", "manga": str(manga_id_fn(soup(url)))}
    return soup(f"{base_url}/wp-admin/admin-ajax.php", method="post", data=data)