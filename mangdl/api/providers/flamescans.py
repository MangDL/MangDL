scanlator = "Flame Scans"
base_url = "https://flamescans.org"
template = "fs_wp"

rpa = 10

def check_manga(r):
    return not r.select_one(".limit .novelabel")