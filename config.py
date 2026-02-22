import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-123'
    # Default to a local SQLite for immediate running, or use MySQL if set
    # e.g., export DATABASE_URL="mysql+pymysql://root:password@localhost/vacc_pred"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:password@localhost/vacc_pred'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
