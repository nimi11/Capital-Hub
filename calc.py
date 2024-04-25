# auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, User
from datetime import datetime

calc_bp = Blueprint('calc', __name__)

@calc_bp.route('/loan/calculator', methods=['GET', 'POST'])
def calculator():
    def calculator():
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        tenure = int(request.form.get('tenure'))
        
        # Perform loan calculations here
        
        principal_amount = amount
        payment_per_period = calculate_payment_per_period(amount, tenure)
        total_interest_payable = calculate_total_interest_payable(amount, tenure)
        total_amount_payable = principal_amount + total_interest_payable

        return render_template("loancalculator.html", 
                                principal_amount=principal_amount,
                                payment_per_period=payment_per_period,
                                total_interest_payable=total_interest_payable,
                                total_amount_payable=total_amount_payable)
    return render_template("loancalculator.html")

def calculate_payment_per_period(amount, tenure):
    # Perform calculation for payment per period
    # You can implement your logic here
    return payment_per_period

def calculate_total_interest_payable(amount, tenure):
    # Perform calculation for total interest payable
    # You can implement your logic here
    return total_interest_payable
