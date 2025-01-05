from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_default_secret_key')  # Use an environment variable for production

# Set up SQLite database (you can change this to another DB for production)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userinfo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User model for the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_n = db.Column(db.String(100))
    last_n = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100))

# Create the tables in the database
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    users = User.query.all()
    return render_template('index1.html', userinfo=users, background_image='desktop.png')

@app.route('/update', methods=['POST'])
def update():
    first_n = request.form.get('first_n', '')
    last_n = request.form.get('last_n', '')
    username = request.form.get('username', '')
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    
    if not all([first_n, last_n, username, email, password]):
        flash('All fields are required.')
        return redirect(url_for('home'))
    
    # Check if the user exists
    user = User.query.filter_by(username=username).first()

    if user:
        # Update the existing user
        user.first_n = first_n
        user.last_n = last_n
        user.email = email
        user.password = password
        flash('User information updated successfully.')
    else:
        # Add a new user
        new_user = User(first_n=first_n, last_n=last_n, username=username, email=email, password=password)
        db.session.add(new_user)
        flash('New user added successfully.')
    
    # Commit the changes to the database
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
