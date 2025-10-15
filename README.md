# URL-Shortener
A simple personal web project to transform long URLs into shorter ones or QR codes. The program uses the TinyURL API service to shorten and format URLs. This web project is built upon the microframework Flask in Python. 
**The website requires an TinyUrl API token.**

## Features
* Includes an user interface that is displayed through the browser.
* Shortens long URLs through the TinyURL API service (requires API token). 
* Ability to copy the shortened URL directly to the clipboard (WIP). 
* Ability to copy QR code from long URL (WIP).
* Stores shortened URLs into an Database to be retrieved to future use.

## Installation
**Clone the repository**
```
git clone https://github.com/FrostyAqua37/URL-Shortener.git
```

**Install the required packages and libraries**
```
pip3 install -r requirements.txt -v
```

**Run following command to execute program**
```
python3 app.py
```


