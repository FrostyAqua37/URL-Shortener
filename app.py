from flask import Flask, render_template, url_for, request, send_file
from flask_sqlalchemy import SQLAlchemy
import qrcode
import qrcode.image.svg
from datetime import datetime
from io import StringIO
import random, string
from urllib.parse import urlparse
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url_history.db'
db = SQLAlchemy(app)
app.app_context().push()
api_token = 'E9Tcq8J30GOorspFf2qumCNzq7BaHyzlw5qOzsF8l7ablxHZzleNIDsobtKi'

class Record(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(255), nullable=False)
    formatted_url = db.Column(db.String(255), nullable=False)
    qr_code = db.Column(db.BLOB, nullable=False)
    date_logged = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        original_url = request.form['original-url']
        try:
            urlparse(original_url)
        except ValueError:
            return "render_template('index.html')"
        else:
            return shorten_url(original_url)
    else:
        return render_template('index.html')

@app.route("/#", methods=['POST', 'GET'])
def retrieve_url():
    if request.method == 'POST':
        original_url = request.form['original-url']
        try:
            parsed_url = urlparse(original_url).query
        except ValueError:
            return "render_template('index.html')"
        else:
            return shorten_url(parsed_url)
    else:
        return render_template('index.html')

def shorten_url(original_link):
    request = {
        'url': original_link,
        'domain': 'http://tinyurl.com/api-create.php',
        'alis': '',
        'tags': '',
        'expires_at': '',
        'description':'string'
    }
    
    try:
        response = requests.get(request)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        return f"Error occurred whilst shortening the URL: {e}"

    else:
        return response.text


def create_qr_code(url_link):
    qr_code = qrcode.make(url_link, image_factory=qrcode.image.svg.SvgImage)

    with open('qr_code.svg', 'wb') as qr:
        qr_code.save(qr)

    img = './static/qr_code.svg'
    return render_template('index.html', img=img)

if __name__ == "__main__":
    app.run(debug=True)