import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "scamshield-default-dev-secret-key-998877")
    DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "scamshield.db"))
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1MB maximum payload for security
    
    # Optional LLM API credentials for hybrid AI analysis
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
    
    # Environment info
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"
    PORT = int(os.getenv("PORT", 5000))
