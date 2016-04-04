from flask import render_template, redirect, request
from app import app, models

@app.route('/')
def index():
    return redirect('/home')

@app.route("/home")
def home():
    return render_template("home.html")
