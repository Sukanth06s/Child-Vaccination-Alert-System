from app import create_app
from models.db_models import db

def reset_database():
    app = create_app()
    with app.app_context():
        print("Dropping all existing tables...")
        db.drop_all()
        print("Recreating tables with the new schema...")
        db.create_all()
        print("Database reset complete.")

if __name__ == '__main__':
    reset_database()
