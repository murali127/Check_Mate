# pages/3_🧾_Cheque_Processing.py
import os
from tempfile import NamedTemporaryFile
from pdf2image import convert_from_path  # Add this import
import streamlit as st
from utils import process_and_crop_cheque, preprocess_image, refine_text_with_gemini, insert_cheque_details, get_db_connection
import pytesseract
from PIL import Image
import json
from datetime import datetime

# Page title
st.title("🧾 Cheque Processing")

# File uploader
uploaded_file = st.file_uploader(
    "Upload Bank Cheque PDF or Image", 
    type=["pdf", "png", "jpg", "jpeg"]
)

if uploaded_file:
    os.makedirs("output_images", exist_ok=True)

    if uploaded_file.type == "application/pdf":
        with NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(uploaded_file.read())
            images = convert_from_path(temp_file.name)
            original_image = images[0].convert("RGB")
    else:
        original_image = Image.open(uploaded_file).convert("RGB")

    col1, col2 = st.columns(2)
    with col1:
        st.image(original_image, caption="Original Cheque", use_container_width=True)

    processed_image = process_and_crop_cheque(original_image)

    with col2:
        st.image(processed_image, caption="Processed Cheque", use_container_width=True)

    processed_image.save(os.path.join("output_images", f"processed_{uploaded_file.name}"))

    processed_image = preprocess_image(processed_image)
    extracted_text = pytesseract.image_to_string(processed_image)

    if extracted_text.strip():
        cheque_data = refine_text_with_gemini(extracted_text)
        
        if cheque_data:
            cheque_data["timestamp"] = datetime.now().isoformat()
            
            st.subheader("🌟 Extracted Cheque Details:")
            st.code(json.dumps(cheque_data, indent=2), language="json")
            
            db, connection_status = get_db_connection()
            st.write(connection_status)
            
            if db is not None:
                inserted_id = insert_cheque_details(db, cheque_data)
                if inserted_id:
                    st.success(f"✅ Cheque details saved to database with ID: {inserted_id}")
                else:
                    st.error("❌ Failed to insert cheque details into the database.")
            else:
                st.error("❌ Failed to connect to MongoDB. Please check your connection settings.")
    else:
        st.error("❌ No text extracted - check image quality.")