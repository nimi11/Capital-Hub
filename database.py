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
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    middlename = db.Column(db.String)
    dob = db.Column(db.DateTime, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    business_name = db.Column(db.String)
    business_sector = db.Column(db.String)
    registration_no = db.Column(db.String)
    bvn = db.Column(db.String)
    business_address = db.Column(db.String)
    home_address = db.Column(db.String)
    state = db.Column(db.String)
    local_government = db.Column(db.String) 
    password = db.Column(db.String, nullable=False)
    
class Verification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    passport = db.Column(db.String(255))
    valid_identification = db.Column(db.String(255))
    tax_statement = db.Column(db.String(255))
    bank_statement = db.Column(db.String(255))
    reference = db.Column(db.String(255))
    relationship = db.Column(db.String(255))
    reference_contact = db.Column(db.String(255))   

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    loan_type = db.Column(db.String, nullable=False)
    loan_amount = db.Column(db.String, nullable=False)
    tenure = db.Column(db.Integer, nullable=False)
    repayment_source = db.Column(db.String, nullable=False)
    bank = db.Column(db.String, nullable=False)
    account_name = db.Column(db.String, nullable=False)
    account_type = db.Column(db.String, nullable=False)
    account_no = db.Column(db.String, nullable=False)
    driver_license = db.Column(db.String, nullable=False)
    bvn = db.Column(db.String, nullable=False)


def init_db():
    with app.app_context():
        db.create_all()
        