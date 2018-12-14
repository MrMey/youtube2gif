import re

URLS = [
    "https://www.youtube.com",
    "https://youtu.be"
]

def is_valid_root_url(url):
    url_idx = 0
    while url_idx < len(URLS):
        if re.match(URLS[url_idx],url):
            return True
        url_idx += 1
    return False
