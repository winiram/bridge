#!flask/bin/python
from app import db, models
db.drop_all()
db.create_all()
