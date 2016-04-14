from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(60), unique=False)
    lname = db.Column(db.String(60), unique=False)
    organization = db.Column(db.String(120), unique=False)
    email = db.Column(db.String(120), unique=False)
    password = db.Column(db.String(20), unique=False)
    search_interfaces = db.relationship('SearchInterface', backref="user")

    def __repr__(self):
        return '<Customer %r>' % self.id

class SearchInterface(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    document_id = db.Column(db.String(120), unique=True)
