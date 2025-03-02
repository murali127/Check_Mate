import os
from dotenv import load_dotenv
import google.generativeai as gemini

# Load environment variables from .env file
load_dotenv()

# Initialize Gemini API with the API key
api_key = os.getenv('GEMINI_API_KEY')
gemini.configure(api_key=api_key)

# Function to refine extracted text using Gemini API
def refine_text_with_gemini(extracted_text):
    """Send the extracted text to Gemini API for correction"""
    try:
        # Create a prompt to ask Gemini to improve or refine the text
        prompt = f"Correct the following text extracted from a cheque: {extracted_text}"

        # Send the prompt to Gemini API to refine the text
        response = gemini.chat(messages=[{"role": "user", "content": prompt}])

        if 'content' in response.choices[0]:
            refined_text = response.choices[0].content.strip()  # Get the corrected text
            return refined_text
        else:
            return extracted_text  # Return original if no correction available
    except Exception as e:
        print(f"Error refining text with Gemini: {e}")
        return extracted_text  # In case of an error, return the original text
