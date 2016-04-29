from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask.ext.login import current_user


#print(SQLALCHEMY_DATABASE_URI)

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = "log_in"

@lm.user_loader
def load_user(user_id):
    """Flask-Login hook to load a User instance from ID."""
    return db.session.query(models.User).get(user_id)

if not app.debug:
    import logging
    from logging import FileHandler
    file_handler = FileHandler("/var/www/bridge/flask.log")
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

from app import views, models

