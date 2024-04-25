from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, User
from datetime import datetime


other_bp = Blueprint('other', __name__)

@other_bp.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'GET':
        return render_template("aboutpage.html")
    
@other_bp.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
            return render_template("productspage.html")

@other_bp.route('/blog', methods=['GET', 'POST'])
def blog():
    if request.method == 'GET':
        return render_template("resources.html")
    
@other_bp.route('/loan/app', methods=['GET', 'POST'])
def loanapplication():
    if request.method == 'GET':
        return render_template("loanapplication.html")
    
@other_bp.route('/customer/support', methods=['GET', 'POST'])
def customer():
    if request.method == 'GET':
        return render_template("customersupport.html")
    
@other_bp.route('/blog/more/1', methods=['GET', 'POST'])
def moreblog():
    if request.method == 'GET':
        return render_template("resources1.html")

@other_bp.route('/blog/more/2', methods=['GET', 'POST'])
def moreblog2():
    if request.method == 'GET':
        return render_template("resources2.html")

