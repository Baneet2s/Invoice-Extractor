from flask import Flask, request, jsonify, render_template, send_file
from extractor import extract_invoice_data
import os
import pandas as pd
import io

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
    Handles multiple file uploads and calls the AI extraction function for each.
    Returns the extracted data as a JSON response.
    """
    if 'files' not in request.files:
        return jsonify({"error": "No files part in the request"}), 400
    
    files = request.files.getlist('files')

    if not files or files[0].filename == '':
        return jsonify({"error": "No files selected"}), 400

    results = []
    for file in files:
        if file:
            try:
                # Read file data and get the content type
                file_data = file.read()
                file_type = file.content_type
                
                extracted_data = extract_invoice_data(file_data, file_type)
                results.append({
                    "filename": file.filename,
                    "data": extracted_data
                })

            except Exception as e:
                print(f"An error occurred during extraction of {file.filename}: {e}")
                results.append({
                    "filename": file.filename,
                    "data": {"error": f"An error occurred: {str(e)}"}
                })
    
    return jsonify(results)

@app.route('/api/export', methods=['POST'])
def export_data():
    """
    Receives JSON data and returns it as a downloadable CSV file.
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Create a list of dictionaries to handle line items
        rows = []
        for result in data:
            filename = result.get('filename')
            extracted_data = result.get('data')

            if extracted_data.get('line_items'):
                for item in extracted_data['line_items']:
                    row = {
                        'filename': filename,
                        'vendor_name': extracted_data.get('vendor_name'),
                        'invoice_date': extracted_data.get('invoice_date'),
                        'invoice_number': extracted_data.get('invoice_number'),
                        'total_amount': extracted_data.get('total_amount'),
                        'currency': extracted_data.get('currency'),
                        'item_description': item.get('description'),
                        'item_quantity': item.get('quantity'),
                        'item_unit_price': item.get('unit_price')
                    }
                    rows.append(row)
            else:
                rows.append({
                    'filename': filename,
                    'vendor_name': extracted_data.get('vendor_name'),
                    'invoice_date': extracted_data.get('invoice_date'),
                    'invoice_number': extracted_data.get('invoice_number'),
                    'total_amount': extracted_data.get('total_amount'),
                    'currency': extracted_data.get('currency'),
                    'item_description': None,
                    'item_quantity': None,
                    'item_unit_price': None
                })
        
        df = pd.DataFrame(rows)
        
        # Create a CSV in memory
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        
        return send_file(
            io.BytesIO(csv_buffer.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name='extracted_invoices.csv'
        )

    except Exception as e:
        print(f"An error occurred during export: {e}")
        return jsonify({"error": "An internal server error occurred during export"}), 500

if __name__ == '__main__':
    app.run(debug=True)