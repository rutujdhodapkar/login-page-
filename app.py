from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import os


app.secret_key = 'your_secret_key_here'  # Set the secret key to something unique and secret

# Ensure the CSV file exists
csv_file_path = 'userinfo.csv'
if not os.path.exists(csv_file_path):
    pd.DataFrame(columns=['first_n', 'last_n', 'username', 'email', 'password']).to_csv(csv_file_path, index=False)

@app.route('/')
def home():
    userinfo = pd.read_csv(csv_file_path)
    return render_template('index1.html', userinfo=userinfo.to_html(index=False), background_image='desktop.png')

@app.route('/update', methods=['POST'])
def update():
    # Use get method with default value to avoid KeyError
    first_n = request.form.get('first_n', '')
    last_n = request.form.get('last_n', '')
    username = request.form.get('username', '')
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    
    # Check if all required fields are provided
    if not all([first_n, last_n, username, email, password]):
        flash('All fields are required.')
        return redirect(url_for('home'))
    
    userinfo = pd.read_csv(csv_file_path)
    
    # Check if the username already exists
    if username in userinfo['username'].values:
        # Update the existing entry
        userinfo.loc[userinfo['username'] == username, ['first_n', 'last_n', 'email', 'password']] = [first_n, last_n, email, password]
        flash('User information updated successfully.')
    else:
        # Append the new entry
        new_entry = pd.DataFrame([[first_n, last_n, username, email, password]], columns=['first_n', 'last_n', 'username', 'email', 'password'])
        userinfo = pd.concat([userinfo, new_entry], ignore_index=True)
        flash('New user added successfully.')
    
    # Write the updated data back to the CSV file
    try:
        userinfo.to_csv(csv_file_path, index=False)
    except PermissionError:
        # Handle the permission error
        print(f"Permission denied: Unable to write to {csv_file_path}. Please check file permissions.")
        return "Error: Unable to update user information due to file permission issues.", 500
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
