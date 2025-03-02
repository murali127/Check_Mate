from dotenv import load_dotenv
import os

load_dotenv()  # Ensure this is called to load the .env file

print("MONGO_URI:", os.getenv("MONGO_URI"))
