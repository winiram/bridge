from flask import Flask
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')

from app import views, models
