# app.py
from flask import Flask, request, jsonify, render_template
from extractor import extract_invoice_data
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """
    Renders the main page of the application.
    """
    return render_template('index.html')

@app.route('/api/extract', methods=['POST'])
def extract():
    """
    Handles the file upload and calls the AI extraction function.
    Returns the extracted data as a JSON response.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
 
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file:
        try:
            image_data = file.read()
            
            extracted_data = extract_invoice_data(image_data)
            
            return jsonify(extracted_data)

        except Exception as e:
            # If any error occurs during the process, return a generic server error.
            print(f"An error occurred during extraction: {e}")
            return jsonify({"error": "An internal server error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)

