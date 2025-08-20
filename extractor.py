import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import io
import json
import pymupdf as fitz # Corrected import statement

load_dotenv()

try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
except Exception as e:
    print(f"Error configuring Gemini API: {e}")

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    try:
        response = model.generate_content([input_prompt, image])
        return response.text
    except Exception as e:
        print(f"Error during API call: {e}")
        return None

def extract_invoice_data(file_data, file_type):
    try:
        if file_type == 'application/pdf':
            # Handle PDF files by converting the first page to an image
            # Use the 'fitz' alias from the corrected import
            pdf_document = fitz.open(stream=file_data, filetype='pdf')
            page = pdf_document.load_page(0)
            # Render the page to a PNG image
            pix = page.get_pixmap(dpi=300)
            image_bytes = pix.tobytes("png")
            image = Image.open(io.BytesIO(image_bytes))
        elif file_type.startswith('image/'):
            # Handle image files directly
            image = Image.open(io.BytesIO(file_data))
        else:
            return {"error": "Unsupported file type. Please upload an image or a PDF."}

        input_prompt = """
        You are an expert in understanding and extracting data from invoices.
        Your task is to analyze the provided invoice image and extract the key information.
        Please output the data in a clean, structured JSON format.

        The JSON object must contain the following keys:
        - "vendor_name": The name of the company that sent the invoice.
        - "invoice_date": The date the invoice was issued (in YYYY-MM-DD format).
        - "invoice_number": The unique identifier for the invoice.
        - "total_amount": The final total amount due, as a number (float).
        - "currency": The currency of the total amount (e.g., USD, INR).
        - "line_items": A list of all items, where each item is an object with "description", "quantity", and "unit_price".

        Return ONLY the JSON object. Do not include any introductory text, explanations, or markdown formatting like ```json.
        """
        response_text = get_gemini_response(input_prompt, image)

        if response_text:
            # Clean up the response if the model adds markdown
            if "```json" in response_text:
                response_text = response_text.replace("```json\n", "").replace("```", "")
            return json.loads(response_text)
        else:
            return {"error": "Failed to get a response from the AI model."}

    except Exception as e:
        print(f"An error occurred in extract_invoice_data: {e}")
        return {"error": f"An error occurred: {str(e)}"}