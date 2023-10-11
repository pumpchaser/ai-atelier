# Technical Design/Project Management List

1. Setup Flask
  - dotenv - store google api keys
  - oauthlib
  - requests
  - openapi/connexion (nice to have) - good for defining/validating api request/response

2. Signup for Google Gmail API
  - https://developers.google.com/gmail/api/guides
  - https://console.cloud.google.com/apis/dashboard?pli=1

3. Setup  GET /connect/email?email=[EMAIL] endpoint
  - create interface for different email providers
  - implement google oauth provider
  - redirect/return Google Auth URL

4. Setup POST(?) /callback endpoint
  - call google to exchange auth code for access token
  - store access token
    - should be stored properly in a database

        ```
        class User(db.Model):
          id = db.Column(db.Integer, primary_key=True)
          email = db.Column(db.String(120), unique=True, nullable=False)
          access_token = db.Column(db.String(200), nullable=False)
          auth_provider = db.Column(db.String(50), nullable=False)
          ```

    - go save time just store in global state if team is okay with it

        `global_data = {} `


Future:

Docker/Containerization - solves the "works on my env" problem, useful for cicd
Alembic - database migrations + database for storing access token securely
