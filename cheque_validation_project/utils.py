# utils.py
import os
import re
import json
import logging
from tempfile import NamedTemporaryFile
from datetime import datetime

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from pdf2image import convert_from_path
import google.generativeai as gen_ai
from dotenv import load_dotenv
from pymongo import MongoClient, WriteConcern
from pymongo.errors import ConnectionFailure

from border_processing import ChequeBorderProcessor

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()]
)

# MongoDB connection details
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "cheque_processing_db"
COLLECTION_NAME = "cheque_details"

# Initialize border processor
border_processor = ChequeBorderProcessor(output_size=(800, 400))

# Image processing functions
def preprocess_image(image):
    """Enhance image quality for OCR processing."""
    image = image.convert("L")
    image = image.filter(ImageFilter.SHARPEN)
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(2)

def process_and_crop_cheque(uploaded_image):
    """Detect and crop cheque borders using OpenCV."""
    try:
        cv_image = cv2.cvtColor(np.array(uploaded_image), cv2.COLOR_RGB2BGR)

        with NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            uploaded_image.save(temp_file.name)
            output_path = os.path.join("output_images", f"processed_{os.path.basename(temp_file.name)}")

            if border_processor.process_image(temp_file.name, output_path):
                processed_image = cv2.imread(output_path)
                return Image.fromarray(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB))

        return uploaded_image

    except Exception as e:
        logging.warning(f"Border detection failed: {str(e)}")
        return uploaded_image

def process_pdf(uploaded_file):
    """Process each page of the uploaded PDF and return processed images."""
    images = convert_from_path(uploaded_file)
    processed_images = []

    for i, image in enumerate(images):
        processed_image = process_and_crop_cheque(image)
        processed_images.append(processed_image)
        processed_image.save(os.path.join("output_images", f"processed_page_{i + 1}.jpg"))

    return processed_images

# Text processing functions
def extract_cheque_info(text):
    """Extract cheque details using regex."""
    cheque_info = {
        "chequeNumber": re.search(r"\b(\d{6,12})\b", text),
        "accountNumber": re.search(r"\b(\d{10,16})\b", text),
        "amount_numbers": re.search(r"\b(\d{1,3}(?:,\d{3})*\.\d{2})\b", text),
        "amount_words": re.search(r"(?i)(?:Rupees|INR|Amount|Rs\.)\s+([a-zA-Z\s-]+)", text),
        "date": re.search(r"\b(\d{2}/\d{2}/\d{4})\b", text),
        "payee": re.search(r"Pay(?: to|ee)?[:\s]+(.+)", text, re.IGNORECASE),
        "bank": re.search(r"Bank[:\s]*(.*)", text, re.IGNORECASE),
    }

    extracted_details = {field: match.group(1) if match else None for field, match in cheque_info.items()}
    return extracted_details

def refine_text_with_gemini(extracted_text):
    """Use Gemini API to refine extracted text."""
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logging.error("❌ Gemini API Key not found! Please set the GEMINI_API_KEY environment variable.")
            return None

        gen_ai.configure(api_key=api_key)  # Configure Gemini with the API key
        model = gen_ai.GenerativeModel("gemini-2.0-flash")
        prompt = f"""
Extract and structure the following cheque details in JSON format with the fields below. The extracted text is messy and fragmented, so carefully analyze and connect the relevant parts to extract the correct values. If a field is not found, leave it as an empty string (""), not null.

Fields:
- chequeNumber: The cheque number (a numeric value, typically 6-12 digits).
- accountNumber: The account number (a numeric value, typically 10-16 digits).
- amount in numbers: The amount in numeric format (e.g., 1000.00).
- amount in words: The amount in words (e.g., "One thousand only").
- date: The date on the cheque. It can be in any of the following formats:
  - `DD-MM-YYYY` (e.g., 10-02-2015)
  - `DD/MM/YYYY` (e.g., 10/02/2015)
  - `DD MM YYYY` (e.g., 10 02 2015)
  - `DDth Month YYYY` (e.g., 10th February 2015)
  - `Month DD, YYYY` (e.g., February 10, 2015)
  - `YYYY-MM-DD` (e.g., 2015-02-10)
  - Abbreviated formats (e.g., 10-Feb-2015 or 10/Feb/2015)
  If the date is fragmented or mixed with other text (e.g., "Date_10- 02-15" or "10-02-2015 fests"), extract only the date part.
- payee: The name of the payee (the person or entity to whom the cheque is issued).
- bank: The name of the bank (e.g., "State Bank of India").

Now, extract the details from the following extracted text:
{extracted_text}
"""

        response = model.generate_content(prompt)

        if response and hasattr(response, "candidates") and response.candidates:
            candidate = response.candidates[0]

            if hasattr(candidate, "content") and hasattr(candidate.content, "parts") and candidate.content.parts:
                refined_text = candidate.content.parts[0].text
                refined_text = refined_text.replace("```json", "").replace("```", "").strip()
                
                try:
                    cheque_data = json.loads(refined_text)
                    return cheque_data
                except json.JSONDecodeError as e:
                    logging.error(f"Error parsing JSON: {e}")
                    return None

        logging.warning("Gemini returned an empty response.")
        return None

    except Exception as e:
        logging.error(f"Error with Gemini API: {e}")
        return None

# MongoDB functions
def get_db_connection():
    """Establish a connection to MongoDB."""
    try:
        logging.info("Attempting to connect to MongoDB...")
        client = MongoClient(MONGO_URI)
        client.admin.command('ping')  # Test the connection
        db = client[DB_NAME]
        logging.info("✅ Connected to MongoDB successfully!")
        return db, "✅ Connected to MongoDB successfully!"
    except ConnectionFailure as e:
        logging.error(f"⚠️ MongoDB connection failed: {e}")
        return None, f"⚠️ MongoDB connection failed: {e}"
    except Exception as e:
        logging.error(f"⚠️ Unexpected error during MongoDB connection: {e}")
        return None, f"⚠️ Unexpected error during MongoDB connection: {e}"

def insert_cheque_details(db, cheque_data):
    """Insert cheque details into the MongoDB collection."""
    try:
        write_concern = WriteConcern(w="majority")
        collection = db[COLLECTION_NAME].with_options(write_concern=write_concern)
        
        logging.info("Attempting to insert cheque data into collection: %s", collection.full_name)
        logging.info("Cheque data: %s", cheque_data)
        
        result = collection.insert_one(cheque_data)
        
        if result.inserted_id:
            logging.info(f"Cheque details inserted with ID: {result.inserted_id}")
            return result.inserted_id
        else:
            logging.error("Failed to insert cheque details.")
            return None
    except Exception as e:
        logging.error(f"Error inserting cheque details: {e}")
        return None