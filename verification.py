import os
from flask import Blueprint, request, redirect, url_for, render_template, flash,session
from werkzeug.utils import secure_filename
from database import db, Verification, User, Loan

verification_bp = Blueprint('verification', __name__)

UPLOAD_FOLDER = 'static'

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@verification_bp.route('/verification', methods=['GET', 'POST'])
def verification():
    email = request.args.get('email')
    if request.method == 'POST':
         # Get user_id from session
        user_id = session.get('user_id')

        # Ensure user is logged in
        if not user_id:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))

        # Get form data
        passport = request.files['passport']
        valid_identification = request.files['identification']
        tax_statement = request.files['tax_statement']
        bank_statement = request.files['bank_statement']
        reference = request.form['reference']
        relationship = request.form['relationship']
        reference_contact = request.form['reference_contact']
        email = request.form.get('email')

        # Check if all required files are provided
        if not (passport and valid_identification and tax_statement and bank_statement):
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
        identification_filename = secure_filename(valid_identification.filename)
        tax_statement_filename = secure_filename(tax_statement.filename)
        bank_statement_filename = secure_filename(bank_statement.filename)

        passport.save(os.path.join(user_dir, passport_filename))
        valid_identification.save(os.path.join(user_dir, identification_filename))
        tax_statement.save(os.path.join(user_dir, tax_statement_filename))
        bank_statement.save(os.path.join(user_dir, bank_statement_filename))

        # Save verification documents to the database
        verification_doc = Verification(
            user_id=user_id,
            passport=passport_filename,
            valid_identification=identification_filename,
            tax_statement=tax_statement_filename,
            bank_statement=bank_statement_filename,
            reference=reference,
            relationship=relationship,
            reference_contact=reference_contact
        )

        db.session.add(verification_doc)
        db.session.commit()

        flash('Verification documents uploaded successfully', 'success')
        return redirect(url_for('verification.loan'))

    return render_template('verification.html' , email=email)

@verification_bp.route('/loan/details' , methods=['GET', 'POST'])
def loan():
# Retrieve user_id from session
    user_id = session.get('user_id')

    # Ensure user is logged in
    if not user_id:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        # Get form data
        loan_type = request.form['loan_type']
        loan_amount = request.form['loan_amount']
        tenure = request.form['tenure']
        repayment_source = request.form['repayment_source']
        bank = request.form['bank']
        account_name = request.form['account_name']
        account_type = request.form['account_type']
        account_no = request.form['account_no']
        driver_license = request.form['driver_license']
        bvn = request.form['bvn']

        # Validate form data
        if len(account_no) != 10:
            flash('Account number must be 10 digits long.', 'error')
            return redirect(request.url)
        if len(driver_license) > 8:
            flash('Driver license number must not exceed 8 characters.', 'error')
            return redirect(request.url)
        if int(tenure) > 12 or int(tenure) < -1:
            flash('Invalid tenure value. Tenure must be between -1 and 12 months.', 'error')
            return redirect(request.url)
        if len(bvn) != 11:
            flash('BVN must be 11 digits long.', 'error')
            return redirect(request.url)

        # If validation passes, save loan details to database
        new_loan = Loan(
            user_id=user_id,
            loan_type=loan_type,
            loan_amount=loan_amount,
            tenure=tenure,
            repayment_source=repayment_source,
            bank=bank,
            account_name=account_name,
            account_type=account_type,
            account_no=account_no,
            driver_license=driver_license,
            bvn=bvn
        )
        db.session.add(new_loan)
        db.session.commit()

        flash('Loan details saved successfully!', 'success')
        return redirect(url_for('verification.success'))

    return render_template('loan.html')

@verification_bp.route('/success')
def success():
    return render_template("success.html")