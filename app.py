import os

from dotenv import load_dotenv
from flask import Flask, redirect, request, session
from google.oauth2.credentials import Credentials
from requests_oauthlib import OAuth2Session
from googleapiclient.discovery import build
from flask_caching import Cache

load_dotenv()  # Load environment variables from .env file
app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)
app.secret_key = os.getenv('FLASK_SECRET')

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
AUTH_BASE_URL = 'https://accounts.google.com/o/oauth2/auth'
TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
SCOPE=['openid', 'profile', 'https://www.googleapis.com/auth/gmail.readonly']

# TODO: Implement OAuth and move to controllers directory
@app.route('/')
def index():
    google = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
    authorization_url, state = google.authorization_url(AUTH_BASE_URL, access_type='offline')
    print(authorization_url)
    session['oauth_state'] = state
    cache.set('oauth_state', state)
    return redirect(authorization_url)


@app.route('/callback')
def callback():
    state = session.get('oauth_state', cache.get('oauth_state'))
    google = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, state=state)
    token = google.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=request.url)

    # Dunno why I have to do this for now
    token['client_id'] = CLIENT_ID
    token['client_secret'] = CLIENT_SECRET

    creds = Credentials.from_authorized_user_info(token, SCOPE)
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()

    if 'messages' in results:
        for message in results['messages']:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            internal_date = msg['internalDate']
            print(f"Email received on: {internal_date}")  # Print the received date

    response = google.get('https://www.googleapis.com/gmail/v1/users/me/profile')
    profile_data = response.json()
    email = profile_data['emailAddress']

    print('results', results)
    return {}
