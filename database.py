# database.py
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///capitalhub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'yWNZU7s8'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define your models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    
class Verification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passport = db.Column(db.String(255))
    valid_identification = db.Column(db.String(255))
    tax_statement = db.Column(db.String(255))
    bank_statement = db.Column(db.String(255))
    reference = db.Column(db.String(255))
    relationship = db.Column(db.String(255))
    reference_contact = db.Column(db.String(255))   

def init_db():
    with app.app_context():
        db.create_all()
        