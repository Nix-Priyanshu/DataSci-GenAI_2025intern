import os
from dotenv import load_dotenv

load_dotenv()

# --- INITIALIZATION ---
# Using the new Client and modern model string
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_ID = os.getenv("MODEL_ID", "gemini-2.0-flash")

# Validate API key
def validate_config():
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY not found. Check or Set it in .env or environment variables."
        )
