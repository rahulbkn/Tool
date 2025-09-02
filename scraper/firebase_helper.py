import firebase_admin
from firebase_admin import credentials, db
import json
import os

# Load Firebase key from environment variable
firebase_key_json = os.environ.get("FIREBASE_KEY_JSON")
if not firebase_key_json:
    raise Exception("FIREBASE_KEY_JSON not set")

cred_dict = json.loads(firebase_key_json)
cred = credentials.Certificate(cred_dict)

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://YOUR_PROJECT_ID.firebaseio.com/'
})

def push_to_firebase(urls, node="wallpapers"):
    ref = db.reference(node)
    for url in urls:
        ref.push({"url": url})
