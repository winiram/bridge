from flask import render_template, redirect, request
from app import app, models

@app.route('/')
def index():
    return redirect('/main')

@app.route("/main")
def home():
    return render_template("main.html")
