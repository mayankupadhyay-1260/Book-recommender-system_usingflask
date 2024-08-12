from flask import Flask, render_template, request, redirect, url_for, jsonify
from model.recommendation_model import recommend
import pandas as pd
import json
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)




# Load existing users from JSON file
users_file = r'users.json'
if os.path.exists(users_file):
    with open(users_file, 'r') as f:
        file_content = f.read()
        if file_content:  # Check if the file is not empty
            users = json.loads(file_content)
        else:
            users = {}
else:
    users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['signup-name']
    email = request.form['signup-email']
    password = request.form['signup-password']
    confirm_password = request.form['signup-confirm-password']
    if password != confirm_password:
        return render_template('index.html', notification="Passwords do not match", notification_type="error")
    if email in users:
        return render_template('index.html', notification="Email already exists", notification_type="error")
    for user in users.values():
        if user['name'] == name:
            return render_template('index.html', notification="Name already exists", notification_type="error")
        if user['password'] == password:
            return render_template('index.html', notification="Password already exists", notification_type="error")
    users[email] = {'name': name, 'password': password}
    with open(users_file, 'w') as f:
        json.dump(users, f)
    return render_template('index.html', notification="Signed up successfully", notification_type="success")

@app.route('/login', methods=['POST'])
def login():
    email = request.form['login-email']
    password = request.form['login-password']
    if email in users and users[email]['password'] == password:
        return redirect(url_for('bookrecommend'))  # Redirect to bookrecommend page if login is successful
    else:
        return render_template('index.html', notification="Invalid login credentials", notification_type="error")

@app.route('/bookrecommend')
def bookrecommend():
    return render_template('bookrecommend.html')

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    genres = data.get('genre')
    if genres:
        recommendations = recommend(genres)
        return jsonify(recommendations)
    else:
        return jsonify({'error': 'No genre provided'}), 400
    

@app.route('/manifest.json')
def manifest():
    return app.send_static_file('manifest.json')

@app.route('/service-worker.js')
def service_worker():
    return app.send_static_file('service-worker.js')    

if __name__ == '__main__':
    app.run(host= '0.0.0.0' , port=5000 ,debug=True)
    