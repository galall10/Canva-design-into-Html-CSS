"""
Configuration and environment variables for the Canva to HTML generator
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Model Configuration
OPENROUTER_MODEL = "meta-llama/llama-4-maverick:free"
GEMINI_MODEL = "gemini-2.0-flash-exp"

# Path Configuration
BASE_DIR = Path(__file__).parent
OUTPUT_FOLDER = BASE_DIR / "output"

# Create necessary directories
OUTPUT_FOLDER.mkdir(exist_ok=True)

# Application Settings
MAX_ITERATIONS = 2
DEFAULT_API_PROVIDER = "gemini" if GEMINI_API_KEY else "openrouter"