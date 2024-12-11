from flask import Flask, jsonify, request, redirect
from flasgger import Swagger
from src.services.ocrServices import ImageTextExtractor

def upload_image():
    if 'image' not in request.files:
        return jsonify(message="No file part"), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify(message="No selected file"), 400

    extractor = ImageTextExtractor()
    image_bytes = file.read()
    try:
        result = extractor.extract_text_all(image_bytes)
        return jsonify(result)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify(message=f"Error processing image: {str(e)}"), 500
