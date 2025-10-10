from flask import Flask, render_template, url_for, request, send_file, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import qrcode
import qrcode.image.svg
from datetime import datetime
import requests
import constants
import validators

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url_history.db'
db = SQLAlchemy(app)
app.app_context().push()
app.secret_key= constants.app_secret_key
error_message = None

class Record(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(255), nullable=False)
    formatted_url = db.Column(db.String(255), nullable=False)
    qr_code = db.Column(db.BLOB, nullable=False)
    date_logged = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/", methods=['POST', 'GET'])
def validate_url():
    if request.method == 'POST':
        original_url = request.form['original-url']
        try:
            if not validators.url(original_url):
                error_message = 'Error: Invalid URL Link.'
                flash(error_message)        
                return render_template('index.html', error=error_message)
        except ValueError:
            return render_template('index.html')
        else:
            flash(shorten_url(original_url))
            return redirect(url_for('index'))
    else:
        return render_template('index.html')
    
def shorten_url(original_link):
    try:
        headers = {
            'Authorization': f'Bearer {constants.tiny_url_token}',
            'Content-Type': 'application/json'
        }

        data = {
            'url': original_link,
            'domain': 'tinyurl.com',
        }
        response = requests.post(url='https://api.tinyurl.com/create', headers=headers, json=data)

    except requests.exceptions.RequestException as error:
        flash(error)
        return render_template('index.html', error=error)
    else:
        data = response.json()
        match response.status_code:
            case 200:      
                return data['data']['tiny_url']
            
            case 422:
                error_message = 'Error: Invalid URL link or Alias field is too long.'
                flash(error_message)
                return render_template('index.html', error=error_message)
        
            case _:
                error_message = 'Error: Something went wrong, please try again.'
                flash(error_message)
                return render_template('index.html', error=error_message)
               
def create_qr_code(url_link):
    ...

def store_record():
    ...

def delete_record():
    ...

def update_record():
    ...

def retrieve_record():
    ...

if __name__ == "__main__":
    app.run(debug=True)