# server.py
# This file is the entry point to your application. When you want to start your Flask server, you run this file. 
# It imports the Flask app instance from config.py, applies CORS (Cross Origin Resource Sharing) settings, and then starts the server.

from flask_cors import CORS
from config import app, db
import routes  # Import your routes module

CORS(app)

if __name__ == '__main__':
    app.run(debug=True)