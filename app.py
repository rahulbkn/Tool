import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "scraper"))

from flask import Flask, request, jsonify
from pinterest_scraper import PinterestScraper
from firebase_helper import push_to_firebase

app = Flask(__name__)
scraper = PinterestScraper()

# Root route for health check
@app.route("/")
def home():
    return "Pinterest Scraper API is running!"

# Main API route
@app.route("/fetch_wallpapers", methods=["GET"])
def fetch_wallpapers():
    query = request.args.get("query", "mobile wallpaper")
    count = int(request.args.get("count", 10))

    try:
        urls = scraper.scrape_wallpapers(query, count)
        push_to_firebase(urls)
        return jsonify({"urls": urls, "count": len(urls)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Development server (debug=False for safety)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
