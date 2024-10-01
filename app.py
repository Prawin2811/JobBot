from flask import Flask, request, jsonify, send_from_directory
import requests
from flask_cors import CORS
import logging
from PyPDF2 import PdfReader

app = Flask(__name__)
CORS(app)

# Setup logging
logging.basicConfig(level=logging.DEBUG)

API_KEY = "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"
API_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

pdf_text = ""

@app.route('/')
def serve_index():
    return send_from_directory('templates', 'index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    if not pdf_text and "resume" in user_message.lower():
        return jsonify({"response": "Please upload a resume first."}), 400
    
    # Create a prompt based on user query and available resume text
    if "resume" in user_message.lower() and pdf_text:
        user_message = f"Extract the following from this resume and format it in a structured way with bullet points: {user_message}. Resume text: {pdf_text}"

    logging.debug(f"User message received: {user_message}")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [
            {"role": "user", "content": user_message}
        ],
        "model": "mixtral-8x7b-32768",
        "max_tokens": 1000
    }

    try:
        response = requests.post(API_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()
        bot_message = response_data.get("choices")[0]["message"]["content"]

        # Ensure the response is formatted as bullet points
        formatted_message = bot_message.replace("\n", "<br>")  # Replace new lines with <br> for HTML rendering
        return jsonify({"response": formatted_message})
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return jsonify({"response": "Sorry, something went wrong."}), 500

@app.route('/api/upload', methods=['POST'])
def upload_pdf():
    global pdf_text
    if 'file' not in request.files:
        return jsonify({"success": False, "response": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "response": "No selected file"}), 400

    try:
        pdf_reader = PdfReader(file)
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text() or ""
        logging.debug(f"Extracted text from PDF: {pdf_text[:500]}")  # Log only a portion for debugging
        return jsonify({"success": True, "response": "Resume uploaded successfully."})
    except Exception as e:
        logging.error(f"Error reading PDF: {e}")
        return jsonify({"success": False, "response": "Sorry, something went wrong while uploading the PDF."}), 500

if __name__ == '__main__':
    app.run(debug=True)
