from flask.sessions import SecureCookieSessionInterface
from vulnQuest import app  # Import the Flask app from vulnQuest.py

# Create a new instance of your Flask app's session interface
session_serializer = SecureCookieSessionInterface().get_signing_serializer(app)

# Admin session data you want to inject
# Encode session data
