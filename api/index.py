import sys
import os

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask app
from multi_tenant_app import app

# This is the WSGI application Vercel will call
application = app

# Also export as app for compatibility
app = application