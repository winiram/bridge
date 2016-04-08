from flask import render_template, redirect, request
from app import app, models

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
