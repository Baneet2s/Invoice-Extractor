## AI Invoice Extractor 

This project is an **AI-powered document processing service** that automates the extraction of key information from invoices. It directly solves the business problem of **manual data entry**, a time-consuming and error-prone task.

### 🚀 Live Demo

You can view and test the live application here:
**[https://invoice-extractor-xxj4.onrender.com/](https://invoice-extractor-xxj4.onrender.com/)**

### 🎯 Key Features & Use Case

  * **Automated Data Extraction:** The core function uses AI to read unstructured data from a document and convert it into structured JSON.
  * **Real-World Application:** This tool can significantly reduce manual labor in finance and accounting departments by automating invoice processing at a large scale.
  * **Minimal & Focused:** Designed as a robust proof-of-concept to showcase key skills without unnecessary features, prioritizing quality over complexity.

### 💻 How It Works

1.  **User Uploads a Document:** A user uploads a document image via the web interface. 
2.  **AI Processes the Data:** The backend sends the image to the **Google Gemini Pro Vision API** to intelligently read the document's content. 
3.  **JSON Output:** The extracted information is returned to the user in a clean, structured JSON format. 

### ⚙️ Technologies Used

  * **Backend:** Python, Flask
  * **AI Model:** Google Gemini Pro Vision API
  * **Containerization:** Docker
  * **Frontend:** HTML, CSS, JavaScript
