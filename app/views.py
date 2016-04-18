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

@app.route("/interface")
def searchInterface():
    return render_template("interface.html")

@app.route("/search")
def searchInterface_side():
    return render_template("search.html")        


@app.route("/test")
def test():
    return render_template("test.html")   