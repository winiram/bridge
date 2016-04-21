from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, PasswordField, FieldList, SelectField
from flask_wtf.html5 import EmailField
from wtforms.validators import DataRequired, Email
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from .util.validators import Unique
from .models import User

class LoginForm(Form):
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    #remember_me = BooleanField('remember_me', default=False)

class SignupForm(Form):
    fname = StringField('fname', validators=[DataRequired()])
    lname = StringField('lname', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email(),
        Unique(User, User.email,message='There is already an account with that email.')])
    password = PasswordField('password', validators=[DataRequired()])

# choices = [('test', 'Test'), ('test2', 'Test')]
display_choices = [('textbox', 'Textbox'), ('dropdown', 'Dropdown')]

class SearchInterfaceForm(Form):
    fieldname = StringField('fieldname', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    # header = SelectField(label='header', choices=choices)
    header =SelectField(label='header')
    display = SelectField(label='display', choices=display_choices)

    def __init__(self, header):
        super(SearchInterfaceForm, self).__init__()
        self.header.choices = header
