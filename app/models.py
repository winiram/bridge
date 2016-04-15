from sqlalchemy.ext.hybrid import hybrid_property
from app import db, lm
from . import bcrypt
from flask.ext.login import UserMixin, current_user

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(60), unique=False)
    lname = db.Column(db.String(60), unique=False)
    email = db.Column(db.String(120), unique=False)
    search_interfaces = db.relationship('SearchInterface', backref="user")
    _password = db.Column(db.String(128))
    authenticated = db.Column(db.Boolean, default=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)

    @lm.user_loader
    def load_user(id):
        return User.query.get(str(id))

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def __repr__(self):
        return '<Customer %r>' % self.id

class SearchInterface(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    document_id = db.Column(db.String(120), unique=True)
