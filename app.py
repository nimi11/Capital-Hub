# app.py
from flask import Flask, render_template
from database import db,app
from flask_migrate import Migrate
from auth import auth_bp
from verification import verification_bp 
# from other_functionality import other_bp



migrate = Migrate(app, db)




# Register blueprints for different functionalities
app.register_blueprint(auth_bp)
app.register_blueprint(verification_bp) 
# app.register_blueprint(other_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
