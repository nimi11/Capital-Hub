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
        amount_str = request.form.get('amount')
        tenure_str = request.form.get('tenure')

        try:
            amount = float(amount_str) if amount_str else 0
            tenure = int(tenure_str) if tenure_str else 0
        except ValueError:
            return redirect(url_for('calc.calculator'))
        
        print("Amount:", amount)
        print("Tenure:", tenure)

        # Perform loan calculations here
        if tenure > 24:
                flash('Maximum tenure allowed is 24 months.', 'calc')
                return redirect(url_for('index'))
        
        principal_amount = "{:,.2f}".format(amount)
        if amount > 0 and tenure > 0:
            # Perform loan calculations only if amount and tenure are greater than zero
            monthly_interest_rate = get_monthly_interest_rate(tenure)
            payment_per_period = calculate_payment_per_period(amount, monthly_interest_rate, tenure)
            total_interest_payable = calculate_total_interest_payable(amount, tenure)
            total_amount_payable = "{:,.2f}".format(round(amount + total_interest_payable, 2))
            payment_per_period = "{:,.2f}".format(round(payment_per_period, 2))
            total_interest_payable = "{:,.2f}".format(round(total_interest_payable, 2))

        return render_template("loancalculator.html", 
                                principal_amount=principal_amount,
                                payment_per_period=payment_per_period,
                                total_interest_payable=total_interest_payable,
                                total_amount_payable=total_amount_payable)
    return render_template("loancalculator.html", 
                                principal_amount=principal_amount,
                                payment_per_period=payment_per_period,
                                total_interest_payable=total_interest_payable,
                                total_amount_payable=total_amount_payable)
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
    return round((r * amount) / (1 - (1 + r) ** -n), 2)

def calculate_total_interest_payable(amount, tenure):
    monthly_interest_rate = get_monthly_interest_rate(tenure)
    payment_per_period = calculate_payment_per_period(amount, monthly_interest_rate, tenure)
    total_payment = round(payment_per_period * tenure, 2)
    total_interest_payable = round(total_payment - amount, 2)
    return total_interest_payable

# def calculate_total_interest_payable(amount, monthly_interest_rate, tenure):
#     payment_per_period = calculate_payment_per_period(amount, monthly_interest_rate, tenure)
#     total_payment = payment_per_period * tenure     
#     total_interest_payable = total_payment - amount
#     return total_interest_payable


