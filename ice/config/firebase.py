import firebase_admin
from firebase_admin import credentials

# Path to your Firebase Admin SDK key
cred = credentials.Certificate("icee-3a0d4-firebase-adminsdk-77c2k-26756a6d82.json")
firebase_admin.initialize_app(cred)
