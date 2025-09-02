import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "scraper"))

from flask import Flask, request, jsonify
from pinterest_scraper import PinterestScraper
from firebase_helper import push_to_firebase

app = Flask(__name__)
scraper = PinterestScraper()

@app.route("/fetch_wallpapers", methods=["GET"])
def fetch_wallpapers():
    query = request.args.get("query", "mobile wallpaper")
    count = int(request.args.get("count", 10))

    urls = scraper.scrape_wallpapers(query, count)
    push_to_firebase(urls)
    
    return jsonify({"urls": urls, "count": len(urls)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
