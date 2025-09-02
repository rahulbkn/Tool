import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase (replace with your key)
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://YOUR_PROJECT_ID.firebaseio.com/'
})

def push_to_firebase(urls, node="wallpapers"):
    ref = db.reference(node)
    for url in urls:
        ref.push({"url": url})