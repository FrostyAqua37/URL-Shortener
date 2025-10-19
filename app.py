from flask import Flask, render_template, url_for, request, send_file, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import qrcode
import qrcode.image.svg
from datetime import datetime
import requests
import constants #Local file with personal API Token.
import validators
from io import BytesIO
from base64 import b64encode

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url_history.db'
db = SQLAlchemy(app)
app.app_context().push()
app.secret_key= constants.app_api_key
error_message = None
original_url = ""

class Urls(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(255), nullable=False)
    short_url = db.Column(db.String(255), nullable=False)
    alias = db.Column(db.String(255), nullable=True)
    date_logged = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/", methods=['POST'])
def format_url():
    original_url = request.form['original-url']
    alias = request.form['alias']
    
    if not validators.url(original_url):
        flash('Error: Invalid URL.')
        return redirect('/')
    else:
        record = Urls.query.filter_by(original_url=f'{original_url}').first()
        if record:
            flash(record.short_url)
        else:
            short_url = shorten_url(original_url, alias)
            new_record = Urls(original_url=original_url, short_url=short_url, alias=alias)
            try:
                db.session.add(new_record)
                db.session.commit()
                flash(short_url)
            except:
                flash('Error: Something went wrong, please try again.')   
        return redirect('/')
        
def shorten_url(original_link, alias=None):
    try:
        headers = {
            'Authorization': f'Bearer {constants.tiny_url_token}',
            'Content-Type': 'application/json'
        }

        data = {
            'url': original_link,
            'domain': 'tinyurl.com',
            'alias' : alias,
        }
        response = requests.post(url='https://api.tinyurl.com/create', headers=headers, json=data)

    except requests.exceptions.RequestException as error:
        flash(error)
        return redirect('/')
    else:
        data = response.json()
        match response.status_code:
            case 200:      
                return data['data']['tiny_url']
            case 401:
                error_message = 'Error: Invalid authorization for this resource. Please check your API token.'
            case 405:
                error_message = 'Error: You do not have permission to access this resource.'
            case 422:
                error_message = 'Error: Invalid URL link or alias is too long.'
            case _:
                error_message = 'Error: Something went wrong, please try again.'

        flash(error_message)            
        return redirect('/')
               
def store_record():
    ...
        
def delete_record():
    ...

def update_record():
    ...

if __name__ == "__main__":
    app.run(debug=True)