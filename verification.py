import os
from flask import Blueprint, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
from database import db, Verification, User

verification_bp = Blueprint('verification', __name__)

UPLOAD_FOLDER = 'static'

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@verification_bp.route('/verification', methods=['GET', 'POST'])
def verification():
    if request.method == 'POST':
        # Get form data
        passport = request.files['passport']
        identification = request.files['identification']
        tax_statement = request.files['tax_statement']
        bank_statement = request.files['bank_statement']
        reference = request.form['reference']
        relationship = request.form['relationship']
        reference_contact = request.form['reference_contact']
        email = request.args.get('email')

        # Check if all required files are provided
        if not (passport and identification and tax_statement and bank_statement):
            flash('Please provide all required documents', 'error')
            return redirect(request.url)

        # Check if the email is provided
        if not email:
            flash('User email not provided', 'error')
            return redirect(url_for('auth.signup'))

        # Get user's directory based on email
        user_dir = os.path.join(UPLOAD_FOLDER, email.split('@')[0])
        os.makedirs(user_dir, exist_ok=True)

        # Save uploaded files to user's directory
        passport_filename = secure_filename(passport.filename)
        identification_filename = secure_filename(identification.filename)
        tax_statement_filename = secure_filename(tax_statement.filename)
        bank_statement_filename = secure_filename(bank_statement.filename)

        passport.save(os.path.join(user_dir, passport_filename))
        identification.save(os.path.join(user_dir, identification_filename))
        tax_statement.save(os.path.join(user_dir, tax_statement_filename))
        bank_statement.save(os.path.join(user_dir, bank_statement_filename))

        # Save verification documents to the database
        verification_doc = Verification(
            passport=passport_filename,
            identification=identification_filename,
            tax_statement=tax_statement_filename,
            bank_statement=bank_statement_filename,
            reference=reference,
            relationship=relationship,
            reference_contact=reference_contact,
            user_email=email
        )

        db.session.add(verification_doc)
        db.session.commit()

        flash('Verification documents uploaded successfully', 'success')
        return redirect(url_for('loan'))

    return render_template('verification.html')

@verification_bp.route('/verification/success')
def loan():
    return render_template('signup3.html')
