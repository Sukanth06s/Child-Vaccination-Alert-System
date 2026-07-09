import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-123'
    # Default to a local SQLite for immediate running, or use MySQL if set
    # e.g., export DATABASE_URL="mysql+pymysql://root:password@localhost/vacc_pred"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///vacc_pred.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Twilio Configuration
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
    
    # Gemini API Configuration
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
