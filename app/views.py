from flask import render_template, redirect, request, session, url_for
from app import app, models
from oauth2client import client
import requests
import json
import os


with open("../client_secret.json") as fin:
    client_secret = json.load(fin)
CLIENT_ID = client_secret["web"]["client_id"]
CLIENT_SECRET = client_secret["web"]["client_secret"]
REDIRECT_URI = "http://localhost:8081/gdrive-token"


@app.route('/')
def index():
    return redirect('/main')

@app.route("/main")
def main():
    return render_template("main.html")

@app.route("/createUpload")
def createUpload():
    return render_template("createUpload.html")

@app.route("/createSearch")
def createSearch():
    return render_template("createSearch.html")

@app.route("/previewSearch")
def previewSearch():
    return render_template("previewSearch.html")

@app.route("/connectGdrive")
def connectGdrive():
    if 'credentials' not in session:
        return redirect('gdrive-token')
    credentials = json.loads(session['credentials'])
    if credentials['expires_in'] <= 0:
        return redirect('gdrive-token')
    else:
        headers = {'Authorization': 'Bearer {}'.format(credentials['access_token'])}
        req_uri = 'https://www.googleapis.com/drive/v2/files'
        r = requests.get(req_uri, headers=headers)
        print(r.text)
        return r.text

@app.route("/gdrive-token")
def gdrive_token():
    if 'code' not in request.args:
        return redirect("https://accounts.google.com/o/oauth2/v2/auth" +\
            "?response_type=code" +\
            "&client_id=" + CLIENT_ID +\
            "&redirect_uri=" + REDIRECT_URI +\
            "&scope=https://www.googleapis.com/auth/drive.readonly" +\
            "&prompt=select_account"
            )
    else:
        auth_code = request.args.get('code')
        data = {'code': auth_code,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code'}
        r = requests.post('https://www.googleapis.com/oauth2/v4/token', data=data)
        session['credentials'] = r.text
        return redirect('connectGdrive')

@app.route("/gdrive-files")
def gdrive_files():
    return
