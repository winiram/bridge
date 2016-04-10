from flask import render_template, redirect, request
from app import app, models
import base64, json, time

test_file_url = 'https://www.filestackapi.com/api/file/S8O2rWoSFewERT8AfNxW'

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

@app.route("/saveFile", methods=["POST"])
def saveFile():
    print("Saved file")
    global test_file_url
    test_file_url = "https://www.filestackapi.com/api/file/" + request.form["url"].split('/')[-1]
    print(test_file_url)
    return "Saved file"

@app.route("/createSearch")
def createSearch():
    return render_template("createSearch.html")

@app.route("/previewSearch")
def previewSearch():
    return render_template("previewSearch.html")
