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
original_url = ""

class Urls(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(255), nullable=False)
    short_url = db.Column(db.String(255), nullable=False)
    qr_code = db.Column(db.BLOB, nullable=False)
    date_logged = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/", methods=['POST'])
def format_url():
    original_url = request.form['original-url']
    if not validators.url(original_url):
        flash('Error: Invalid URL.')
        return redirect('/')
    else:
        query = retrieve_record(original_url)
        if query:
            flash(query)
        else:
            flash(shorten_url(original_url))
        return redirect('/')
        
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
            
            case 401:
                flash('Error: Invalid authorization for this resource. Please check your API token.')

            case 405:
                flash('Error: You do not have permission to access this resource.')

            case 422:
                error_message = 'Error: Invalid URL link or alias is too long.'
                flash(error_message)
        
            case _:
                error_message = 'Error: Something went wrong, please try again.'
                flash(error_message)
            
        return redirect('/')
               
def create_qr(original_link):
    ...

def store_record():
    ...
        
def delete_record():
    ...

def update_record():
    ...

def retrieve_record(url):
    try:
        return Urls.query.filter_by(original_url=url).all()
    except:
        return 

if __name__ == "__main__":
    app.run(debug=True)