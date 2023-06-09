# setup.py
# This file is meant to be run once to set up your database. 
# It imports your Flask app instance and your SQLAlchemy db instance from config.py, 
# then creates all the database tables defined in your models (currently, you only have the Feedback model).
from config import db, app

with app.app_context():
    db.create_all()