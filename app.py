# app.py
from flask import Flask, render_template,request,flash,redirect,url_for
from database import db,app, User
from flask_migrate import Migrate
from auth import auth_bp
from calc import calc_bp
from verification import verification_bp 
from other import other_bp



migrate = Migrate(app, db)




# Register blueprints for different functionalities
app.register_blueprint(auth_bp)
app.register_blueprint(calc_bp)
app.register_blueprint(verification_bp) 
app.register_blueprint(other_bp)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/delete_all_entries', methods=['GET', 'POST'])
def delete_all_entries():
    if request.method == 'GET':
        try:
            # Delete all entries in the User table
            

            # Delete all entries in the Owner table
            db.session.query(User).delete()
            

            # # Commit the changes to the database
            db.session.commit()

           
        except Exception as e:
            # Handle exceptions if any
            print('hello')

        return redirect(url_for('index'))  # Redirect to the home page or any other page

    return render_template('delete_entries.html')  # Create a template for the delete_entries page
         

if __name__ == '__main__':
    app.run(debug=True)
