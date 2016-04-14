from flask import render_template, redirect, request, flash, jsonify
from app import app, models, db, fileprocessing
import base64, json, time
import urllib.request
import pandas as pd
from sqlalchemy import engine

@app.route('/')
def index():
    return redirect('/main')

@app.route("/main")
def main():

    # Waiting for login, create bogus user
    if not models.User.query.first():
        user = models.User(
            fname = "Guest",
            lname = "User",
            organization = "UC Berkeley",
            email = "email.me@berkeley.edu",
            password = "youshouldn't use this"
        )
        db.session.add(user)
        db.session.commit()

    return render_template("main.html")

@app.route("/createUpload")
def createUpload():
    # Temporarily just create one search interface
    if not models.SearchInterface.query.first():
        user = models.User.query.first()
        si = models.SearchInterface()
        user.search_interfaces.append(si)
        db.session.add(user)
        db.session.commit()
    return render_template("createUpload.html")

@app.route("/previewUpload", methods=['POST'])
def previewUpload():
    global test_file_url
    si = models.SearchInterface.query.first()
    file_url = 'https://www.filestackapi.com/api/file/' + si.document_id;
    return render_template("previewUpload.html", url=file_url)

@app.route("/storeFile", methods=["POST"])
def saveFile():
    print("Storing file")
    # Need to do some error checking on file
    file_url = request.form["url"]
    # file_url = 'https://www.filestackapi.com/api/file/QROhdz5ITLOHRKP1mBlr'
    file_id = file_url.split('/')[-1]

    # Get file from filestack, Might need to implement HTTPS
    httpResponse = urllib.request.urlopen(file_url + "/metadata")
    print("The server's response to {} was {}".format(file_url, httpResponse.status))
    file_metadata = json.loads(httpResponse.read().decode("utf-8"))
    mimetype = file_metadata["mimetype"]
    print(mimetype)


    # Check for valid file, if it contains headers.
    df = fileprocessing.load(file_url, mimetype)
    validation = fileprocessing.validate(df)
    if not validation["success"]:
        return jsonify(validation)

    # If file is valid store in database, otherwise return to upload page with error message
    if not db.engine.has_table(file_id):
        df.to_sql(file_id, db.engine, index=False)
        si = models.SearchInterface.query.first() # REPLACE WITH SI ID IN SESSION
        si.document_id = file_id
        db.session.commit()
    else:
        # COMPLETE check if file has been updated and passes test than can add file
        pass

    return jsonify(validation)

@app.route("/createSearch")
def createSearch():
    return render_template("createSearch.html")

@app.route("/previewSearch")
def previewSearch():
    return render_template("previewSearch.html")
