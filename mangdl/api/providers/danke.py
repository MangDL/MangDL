scanlator = "Danke fürs Lesen"
base_url = "https://danke.moe"
template = "guya"

def links_fn(rmh):
    return {"md": rmh("Link").select_one("a")["href"]}