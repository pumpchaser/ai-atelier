# ai-atelier takehome

## Installation

1. Create venv

`$ python3 -m venv .venv`

2. Activate venv

`$ . .venv/bin/activate`

3. Install Flask (TODO: move into script)

`pip install flask oauthlib requests python-dotenv requests_oauthlib pytest`

4. Create a .env file and fill it out with your Google API cred

`cp .env.example .env`

## Local Server

`flask --app app run`


## Tests

`pytest tests/`
