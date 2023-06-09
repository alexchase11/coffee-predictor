# config.py 
# This file is where you create your Flask app instance and configure it, 
# including the database settings. It also defines the database model Feedback. 
# This is the structure of the data you'll be storing in the database.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create the flask app
app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/alexa/coffee-predictor/database/coffeedatabase.db' 
db = SQLAlchemy(app)

# Define the Data Model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.LargeBinary, nullable=False)  # We store images as binary data.
    predicted_roaster = db.Column(db.String(120), nullable=False)
    actual_roaster = db.Column(db.String(120), nullable=True)
    actual_bean = db.Column(db.String(120), nullable=True)
    prediction_correct = db.Column(db.Boolean, nullable=False)

class Roaster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roaster = db.Column(db.String(120), nullable=False)
    bean = db.Column(db.String(120), nullable=False)
    price = db.Column(db.String(120), nullable=False)
    number_of_reviews = db.Column(db.Integer)
    rating = db.Column(db.Float)
    regular_price = db.Column(db.String(120), nullable=False)
    image_urls = db.Column(db.String(1000), nullable=False)