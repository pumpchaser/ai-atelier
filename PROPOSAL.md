# Technical Design/Project Management List

1. Setup Python/Flask
  Reason: The team at Ai-Atelier is looking for a python developer so I want to showcase my python skillset. I chose Flask because it's a lightweight framework that is easy to setup and allows me to meet the project requirement (expose API endpoints)

  Libraries:
    - dotenv - store google api keys
    - oauthlib
    - requests


2. Signup for Google Gmail API
  - https://developers.google.com/gmail/api/guides
  - https://console.cloud.google.com/apis/dashboard?pli=1

3. Setup  GET /connect/email?email=[EMAIL] endpoint
  - create interface for different email providers (inherits from abc interface)
    - we will infer email provider based on email address
    - interface should expose function to:
      1. given timestamp (int), return boolean whether user received email since (after) timestamp
  - implement google oauth provider
  - redirect URL

4. Setup GET /callback endpoint
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

        Note: We can probably infer auth_provider from email but Google today supports

    - just store in global state if team is okay with it to save on time (really bad practice, maybe use redis or cache library)

        `global_data = {} `

5. Setup GET /emails/search
  - accepts access token and timestamp (int)
  - use access token to parse emails and get internal date
  - return true if any email were received after timestamp


5. Deploy on Heroku



Forward Thinking/Additional Features:

Docker/Containerization - solves the "works on my env" problem, also sets us up for CICD

Database (Alembic/Postgres) - potentially start parsing user email and storing it in a DB to avoid a network call on every GET /emails/search

Celery - queue background tasks to fetch user emails' internal date nightly and store in database

Deploy on AWS - more granular control and cheaper than heroku which is fine for free tier demo

OpenAPI/Swagger + connexion - good for defining/validating api request/response

Clean up requirements.txt - I probably have a few unneeded deps that I installed during setup
