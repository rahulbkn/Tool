import requests
from bs4 import BeautifulSoup
import time
import json
from urllib.parse import quote

class PinterestScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36',
        })

    def scrape_wallpapers(self, query, count=5):
        pin_urls = self.get_pin_urls(query, count)
        highres_urls = []
        for pin_url in pin_urls:
            highres_urls.extend(self.get_highres_from_pin(pin_url))
            time.sleep(1)
        return list(dict.fromkeys(highres_urls))[:count]

    def get_pin_urls(self, query, max_pins=10):
        try:
            search_url = f"https://www.pinterest.com/search/pins/?q={quote(query)}"
            resp = self.session.get(search_url, timeout=15)
            soup = BeautifulSoup(resp.text, 'html.parser')
            pin_links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/pin/') and href not in pin_links:
                    pin_links.append(f"https://www.pinterest.com{href}")
                if len(pin_links) >= max_pins:
                    break
            return pin_links
        except:
            return []

    def get_highres_from_pin(self, pin_url):
        try:
            resp = self.session.get(pin_url, timeout=15)
            soup = BeautifulSoup(resp.text, 'html.parser')
            scripts = soup.find_all('script', type='application/json')
            urls = []
            for s in scripts:
                try:
                    if not s.string:
                        continue
                    data = json.loads(s.string)
                    urls.extend(self.extract_highres_from_json(data))
                except:
                    continue
            return urls
        except:
            return []

    def extract_highres_from_json(self, data):
        urls = []
        def recursive(d):
            if isinstance(d, dict):
                if 'url' in d and isinstance(d['url'], str) and 'originals' in d['url']:
                    urls.append(d['url'])
                for v in d.values():
                    recursive(v)
            elif isinstance(d, list):
                for i in d:
                    recursive(i)
        recursive(data)
        return list(set(urls))