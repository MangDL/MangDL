from ..base import soup

scanlator = "Chibimanga"
base_url = "https://www.cmreader.info"
template = "wordpress"

ch_num_fn = "wmcc"
src = "data-src"

def rch_fn(url, manga_id_fn, **kwargs):
    data = {"action": "manga_get_chapters", "manga": str(manga_id_fn(soup(url)))}
    return soup(f"{base_url}/wp-admin/admin-ajax.php", method="post", data=data)