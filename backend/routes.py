# routes.py
# This file is where you define your Flask routes - the endpoints of your web application. 
# When an image file is sent to this endpoint, it uses your trained model to predict the roaster and returns the result.
from config import app, db, Feedback, Roaster
from flask import Flask, request
from flask_cors import CORS
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import pickle
import sklearn 
from PIL import Image
from io import BytesIO

model = load_model('test_model.h5')
with open('encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return 'No file part in the request', 400
    file = request.files['file']

    # Convert the Flask file storage to a BytesIO object
    img_data = BytesIO(file.read())
    
    # Step 1: Read the image file
    img = image.load_img(img_data, target_size=(256, 256))

    # Step 2: Preprocess the image
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0

    # Step 3: Make a prediction
    prediction = model.predict(x)
    predicted_class = np.argmax(prediction)

    # Step 4: Convert the prediction to roaster name
    predicted_roaster = encoder.classes_[predicted_class]

    # Fetch roaster details from the database
    roaster_info = Roaster.query.filter_by(roaster=predicted_roaster).first()

    # If roaster not found in the database, handle accordingly
    if not roaster_info:
        return {
            'prediction': predicted_roaster,
            'roaster_info': None
        }

    # Construct roaster details
    roaster_details = {
        'roaster': roaster_info.roaster,
        'bean': roaster_info.bean,
        'price': roaster_info.price,
        'number_of_reviews': roaster_info.number_of_reviews,
        'rating': roaster_info.rating,
        'regular_price': roaster_info.regular_price,
        'image_urls': roaster_info.image_urls.split(',')  # Assuming multiple URLs are comma-separated
    }

    # Return both the prediction and the roaster details
    return {
        'prediction': predicted_roaster,
        'roaster_info': roaster_details
    }

@app.route('/feedback', methods=['POST'])
def feedback():
    if 'file' not in request.files:
        return 'No file part in the request', 400

    file = request.files['file']
    image_data = BytesIO(file.read())

    predicted_roaster = request.form.get('predicted_roaster')
    actual_roaster = request.form.get('actual_roaster', None)
    actual_bean = request.form.get('actual_bean', None)
    prediction_correct = request.form.get('prediction_correct') == 'true'  # Convert the string to a boolean

    if prediction_correct and actual_roaster is None:
        return 'Actual roaster is missing', 400

    if prediction_correct:
        actual_roaster = predicted_roaster

    feedback = Feedback(
        image=image_data.getvalue(), 
        predicted_roaster=predicted_roaster,
        actual_roaster=actual_roaster,
        actual_bean=actual_bean,
        prediction_correct=prediction_correct
    )
    db.session.add(feedback)
    db.session.commit()

    return 'Feedback submitted', 200

# This following routes are for debugging 
@app.route('/feedbacks', methods=['GET'])
def feedbacks():
    feedbacks = Feedback.query.all()
    all_feedbacks = []
    for feedback in feedbacks:
        feedback_data = {
            "id": feedback.id,
            "predicted_roaster": feedback.predicted_roaster,
            "actual_roaster": feedback.actual_roaster,
            "actual_bean": feedback.actual_bean,
            "prediction_correct": feedback.prediction_correct,
        }
        all_feedbacks.append(feedback_data)

    return {
        'feedbacks': all_feedbacks
    }

# display the most recent images added to the database. 
import io
import base64
from flask import jsonify, send_file

@app.route('/recent_image', methods=['GET'])
def recent_image():
    # Fetch the most recent feedback entry
    feedback = Feedback.query.order_by(Feedback.id.desc()).first()

    if feedback is None:
        return 'No feedback found', 404

    feedback_data = {
        'id': feedback.id,
        'predicted_roaster': feedback.predicted_roaster,
        'actual_roaster': feedback.actual_roaster,
        'actual_bean': feedback.actual_bean,
        'prediction_correct': feedback.prediction_correct,
    }

    # Create a file-like object from the image data
    image_stream = io.BytesIO(feedback.image)

    # Return a JSON response with the feedback data and the image URL
    return jsonify(feedback_data=feedback_data, image_url='/recent_image/image')

@app.route('/recent_image/image', methods=['GET'])
def recent_image_image():
    # Fetch the most recent feedback entry
    feedback = Feedback.query.order_by(Feedback.id.desc()).first()

    if feedback is None:
        return 'No feedback found', 404

    # Create a file-like object from the image data
    image_stream = io.BytesIO(feedback.image)

    return send_file(image_stream, mimetype='image/jpeg')

# Get roasters table
@app.route('/roasters', methods=['GET'])
def roasters():
    roasters = Roaster.query.all()
    all_roasters = []
    for roaster in roasters:
        roaster_data = {
            "id": roaster.id,
            "roaster": roaster.roaster,
            "bean": roaster.bean,
            "price": roaster.price,
            "number_of_reviews": roaster.number_of_reviews,
            "rating": roaster.rating,
            "regular_price": roaster.regular_price,
            "image_urls": roaster.image_urls
        }
        all_roasters.append(roaster_data)

    return {
        'roasters': all_roasters
    }

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file('../frontend/build/index.html')