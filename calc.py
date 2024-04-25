# auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, User
from datetime import datetime

calc_bp = Blueprint('calc', __name__)

@calc_bp.route('/loan/calculator', methods=['GET', 'POST'])
def calculator():
    principal_amount = 0
    payment_per_period = 0
    total_interest_payable = 0
    total_amount_payable = 0
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        tenure = int(request.form.get('tenure'))
        
        # Perform loan calculations here
        if tenure > 24:
                flash('Maximum tenure allowed is 24 months.', 'error')
                return redirect(url_for('calc.calculator'))
        
        principal_amount = amount
 # Perform loan calculations
        monthly_interest_rate = get_monthly_interest_rate(tenure)
        payment_per_period = calculate_payment_per_period(amount, monthly_interest_rate, tenure)
        total_interest_payable = calculate_total_interest_payable(amount, monthly_interest_rate, tenure)
        total_amount_payable = amount + total_interest_payable
        return render_template("loancalculator.html", 
                                principal_amount=principal_amount,
                                payment_per_period=payment_per_period,
                                total_interest_payable=total_interest_payable,
                                total_amount_payable=total_amount_payable)
    return render_template("loancalculator.html")

def get_monthly_interest_rate(tenure):
    if 2 <= tenure <= 6:
        return 0.02 / 12
    elif 7 <= tenure <= 12:
        return 0.025 / 12
    elif 13 <= tenure <= 18:
        return 0.03 / 12
    elif 19 <= tenure <= 24:
        return 0.035 / 12


def calculate_payment_per_period(amount, monthly_interest_rate, tenure):
    n = tenure
    r = monthly_interest_rate
    return (r * amount) / (1 - (1 + r) ** -n)

def calculate_total_interest_payable(amount, tenure):
    payment_per_period = calculate_payment_per_period(amount, monthly_interest_rate, tenure)
    total_payment = payment_per_period * tenure
    total_interest_payable = total_payment - amount
    return total_interest_payable