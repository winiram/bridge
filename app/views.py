from flask import render_template, redirect, request
from app import app, models, db
import base64, json, time
import urllib.request
import pandas as pd


test_file_url = ''

@app.route('/')
def index():
    return redirect('/main')

@app.route("/main")
def main():
    return render_template("main.html")

@app.route("/createUpload")
def createUpload():
    # Should create a security policy to make this safer
    return render_template("createUpload.html")

@app.route("/previewUpload", methods=['POST'])
def previewUpload():
    global test_file_url
    return render_template("previewUpload.html", url=test_file_url)

#@app.route("/storeFile", methods=["POST"])
@app.route("/storeFile")
def saveFile():
    print("Storing file")
    # Need to do some error checking on file
    # file_url = request.form["url"]
    file_url = 'https://www.filestackapi.com/api/file/QROhdz5ITLOHRKP1mBlr'
    file_id = file_url.split('/')[-1]

    # Get file from filestack, Might need to implement HTTPS
    httpResponse = urllib.request.urlopen(file_url + "/metadata")
    file_metadata = json.loads(httpResponse.read().decode("utf-8"))
    print(file_metadata)
    mimetype = file_metadata["mimetype"]

    # Load file into pandas dataframe
    if mimetype == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or mimetype == "application/vnd.ms-excel":
        df = pd.read_excel(file_url)
    elif mimetype == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_csv(file_url)

    # Check for valid file, if it contains headers.
    print("File headers")
    print(df.columns.values)
    # TO COMPLETE

    # If file is valid store in database, otherwise return to upload page with error message (using Flask flash)
    df.to_sql(file_id, db.engine, index=False)

    global test_file_url
    test_file_url = file_url
    print(test_file_url)
    return "Saved file"

@app.route("/createSearch")
def createSearch():
    return render_template("createSearch.html")

@app.route("/previewSearch")
def previewSearch():
    return render_template("previewSearch.html")
