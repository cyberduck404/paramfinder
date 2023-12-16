import sys

import requests
from ratelimit import limits, sleep_and_retry


user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

@sleep_and_retry
@limits(calls=15, period=60)
def fetch(domain, exts, proxy=None, placeholder=None):
    wayback_uri = f"https://web.archive.org/cdx/search/cdx?url={domain}/*&output=txt&collapse=urlkey&fl=original&page=/"
    proxies = {'http': proxy, 'https': proxy}
    headers = {
        'User-Agent': user_agents[0]
    }
    try:
        r = requests.get(wayback_uri, proxies=proxies, headers=headers)
        return r
    except (requests.exceptions.RequestException, ValueError) as e:
        sys.stderr.write(f'[ERR] {domain}: {e}')
    except KeyboardInterrupt:
        sys.stderr.write(f'KeyboardInterrupt')
        sys.exit(0)