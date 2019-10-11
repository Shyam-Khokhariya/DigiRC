import firebase_admin
import pyrebase
import os
from django.conf import settings
from firebase_admin import credentials

firebase_config = {
    'apiKey': "AIzaSyCs4Yq8i4cBGHxFWfDNYkdybcf0DEjEkK0",
    'authDomain': "digirc-scet.firebaseapp.com",
    'databaseURL': "https://digirc-scet.firebaseio.com/",
    'projectId': "digirc-scet",
    'storageBucket': "digirc-scet.appspot.com",
    'messagingSenderId': "483564861009",
    'appId': "1:483564861009:web:2f9ccdf224e51d1f"
}

firebase = pyrebase.initialize_app(firebase_config)

auth = firebase.auth()

database = firebase.database()

storage = firebase.storage()

filepath = os.path.join(settings.BASE_DIR, 'DigiRC//service_account_key.json')
cred = credentials.Certificate(filepath)
firebase_admin.initialize_app(cred)
