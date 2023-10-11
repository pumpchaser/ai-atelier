from flask import Flask, redirect, request, session
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET')

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
AUTH_BASE_URL = 'https://accounts.google.com/o/oauth2/auth'
TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
SCOPE = ['https://www.googleapis.com/auth/gmail.readonly']


# TODO: Implement OAuth and move to controllers directory
@app.route('/')
def index():
    google = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
    authorization_url, state = google.authorization_url(AUTH_BASE_URL, access_type='offline')
    session['oauth_state'] = state
    return redirect(authorization_url)
