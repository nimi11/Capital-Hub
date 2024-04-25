# auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, User
from datetime import datetime


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
     if request.method == 'POST':
        # Get form data
        lastname = request.form.get('lastname')
        firstname = request.form.get('firstname')
        middlename = request.form.get('middlename')
        dob_str = request.form.get('dob')
        dob = datetime.strptime(dob_str, '%Y-%m-%d')
        phonenumber = request.form.get('phonenumber')
        email = request.form.get('email')
        businessname = request.form.get('businessname')
        businesssector = request.form.get('businesssector')
        registrationno = request.form.get('registrationno')
        bvn = request.form.get('bvn')
        businessaddress = request.form.get('businessaddress')
        homeaddress = request.form.get('homeaddress')
        state = request.form.get('state')
        localgovt = request.form.get('localgovt')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        # Check if passwords match
        if password != password2:
            flash('Passwords do not match', 'error')
            return redirect(url_for('auth.signup'))
        
         # Check if the email already exists in the database
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already exists. Please use a different email.', 'error')
            return redirect(url_for('auth.signup'))

        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(password)

        # Create a new user instance with the hashed password
        new_user = User(
            lastname=lastname,
            firstname=firstname,
            middlename=middlename,
            dob=dob,
            phone_number=phonenumber,
            email=email,
            business_name=businessname,
            business_sector=businesssector,
            registration_no=registrationno,
            bvn=bvn,
            business_address=businessaddress,
            home_address=homeaddress,
            state=state,
            local_government=localgovt,
            password=hashed_password
        )

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id

        # Redirect to the login page after successful signup
        flash('Account created successfully. Please log in.', 'success')
        return redirect(url_for('verification.verification', email=email))

     return render_template('signup.html')
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Find the user by email
        user = User.query.filter_by(email=email).first()

        if user:
            # Check if the password matches
            if check_password_hash(user.password, password):
                # Password matches, redirect to dashboard or home page
                session['user_id'] = user.id
                return redirect(url_for('auth.dashboard'))
            else:
                flash('Incorrect email or password', 'error')
                return redirect(url_for('auth.login'))
        else:
            flash('Incorrect email or password', 'error')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
   return render_template("userdashboard4.html")