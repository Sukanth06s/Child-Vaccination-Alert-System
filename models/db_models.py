from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class UserInput(db.Model):
    __tablename__ = 'user_inputs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    child_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    father_name = db.Column(db.String(100))
    mother_name = db.Column(db.String(100))
    
    # Demographics
    v012 = db.Column(db.Integer)
    v106 = db.Column(db.Integer)
    v190 = db.Column(db.Integer)
    v025 = db.Column(db.Integer)
    v101 = db.Column(db.Integer)
    v155 = db.Column(db.Integer)
    v157 = db.Column(db.Integer)
    v158 = db.Column(db.Integer)
    v159 = db.Column(db.Integer)
    v467d = db.Column(db.Integer)
    v481 = db.Column(db.Integer)
    
    # Child features
    b19 = db.Column(db.Integer)
    b4 = db.Column(db.Integer)
    b5 = db.Column(db.Integer)
    bord = db.Column(db.Integer)
    
    # Health Access
    h1 = db.Column(db.Integer)
    v113 = db.Column(db.String(100))
    v116 = db.Column(db.String(100))
    m14 = db.Column(db.Integer)
    m15 = db.Column(db.Integer)
    m17 = db.Column(db.Integer)
    m18 = db.Column(db.Integer)
    
    # Vaccine status fields (h2-h63 approx)
    h0 = db.Column(db.Integer, default=0)
    h2 = db.Column(db.Integer, default=0)
    h50 = db.Column(db.Integer, default=0)
    h3 = db.Column(db.Integer, default=0)
    h4 = db.Column(db.Integer, default=0)
    h5 = db.Column(db.Integer, default=0)
    h6 = db.Column(db.Integer, default=0)
    h7 = db.Column(db.Integer, default=0)
    h8 = db.Column(db.Integer, default=0)
    h9 = db.Column(db.Integer, default=0)
    h9a = db.Column(db.Integer, default=0)
    h51 = db.Column(db.Integer, default=0)
    h52 = db.Column(db.Integer, default=0)
    h53 = db.Column(db.Integer, default=0)
    h57 = db.Column(db.Integer, default=0)
    h58 = db.Column(db.Integer, default=0)
    h59 = db.Column(db.Integer, default=0)
    h61 = db.Column(db.Integer, default=0)
    h62 = db.Column(db.Integer, default=0)
    h63 = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    predictions = db.relationship('Prediction', backref='user', lazy=True)

class Prediction(db.Model):
    __tablename__ = 'predictions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_inputs.id'), nullable=False)
    vaccine_name = db.Column(db.String(50), nullable=False)
    miss_probability = db.Column(db.Float, nullable=False)
    risk_level = db.Column(db.String(10), nullable=False) # LOW, MEDIUM, HIGH
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
