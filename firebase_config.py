
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("hidden-diaries-9c667-firebase-adminsdk-fbsvc-b6ba486eb5")
firebase_admin.initialize_app(cred)

db = firestore.client()
