from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import cv2
import numpy as np
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'})

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'})

    if file:
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)

        # Perform image processing (Example: Convert to grayscale)
        img = cv2.imread(filename)
        processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        processed_filename = 'processed_' + file.filename
        processed_filepath = os.path.join(UPLOAD_FOLDER, processed_filename)
        cv2.imwrite(processed_filepath, processed_img)

        return jsonify({'processedImage': processed_filename})


@app.route('/processed-image/<filename>', methods=['GET'])
def get_processed_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    app.run(debug=True)
