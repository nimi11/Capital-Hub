# auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash
from database import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        phonenumber = request.form.get('number')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        email = request.form.get('email')
        # Check if passwords match
        if password != password2:
            flash('Passwords do not match', 'error')
            return redirect(url_for('signup'))

        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(password)

        # Create a new user instance with the hashed password
        new_user = User(
            email=email,
            password=hashed_password,
            phone_number=phonenumber
    
        )

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        # Redirect to the login page after successful signup
        flash('Account created successfully. Please log in.', 'success')
        return render_template('signup2.html')

    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('signin.html')
