import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Bot configuration."""
    
    # Telegram Bot Token (from @BotFather)
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    
    # OpenAI API Key
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Optional: Use different summarization API
    SUMMARIZATION_API = os.getenv("SUMMARIZATION_API", "openai")
    
    # Summary length options
    SUMMARY_LENGTHS = {
        "short": 50,
        "medium": 100,
        "long": 200
    }
    
    # Default summary length
    DEFAULT_SUMMARY_LENGTH = "medium"
    
    # Max text length to process
    MAX_TEXT_LENGTH = 5000
    
    # Supported document types
    SUPPORTED_DOCUMENTS = ['.txt', '.pdf', '.docx', '.md', '.rtf']
    
    # Logging level
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
