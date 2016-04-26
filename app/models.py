from sqlalchemy.ext.hybrid import hybrid_property
from app import db, lm
from . import bcrypt
from flask.ext.login import UserMixin, current_user
from sqlalchemy import Column
from sqlalchemy.schema import PrimaryKeyConstraint
from enum import Enum


# Accepted SearchFieldTypes
class FieldType(Enum):
    Textbox = "Textbox"
    UniqueSearch = "Dropdown"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(60), unique=False)
    lname = db.Column(db.String(60), unique=False)
    email = db.Column(db.String(120), unique=True)
    search_interfaces = db.relationship('SearchInterface', lazy='dynamic', backref="users")
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
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    document_id = db.relationship("Document", uselist=False, backref="search_interfaces")

class Document(db.Model):
    document_id = db.Column(db.String(120), primary_key=True)
    search_interface = db.Column(db.Integer, db.ForeignKey('search_interface.id'))
    headers = db.relationship("Header",lazy='dynamic', backref="documents")

headers = db.Table('headers',
    db.Column('search_field', db.Integer, db.ForeignKey('search_field.id')),
    db.Column('header', db.String, db.ForeignKey('header.header_name'))
)

class SearchField(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    field_type = db.Column(db.Enum(*FieldType.__members__.keys()))
    name = db.Column(db.String(120))
    description = db.Column(db.Text)
    headers = db.relationship('Header', secondary=headers, backref='search_fields')

class Header(db.Model):
    header_name = db.Column(db.String(120), primary_key=True)
    document = db.Column(db.Integer, db.ForeignKey("document.document_id"))

    __table_args__ = (
        PrimaryKeyConstraint("header_name", "document"),
    )
