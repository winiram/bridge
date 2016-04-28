from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, PasswordField, FieldList, SelectField, SelectMultipleField, FormField, FieldList, BooleanField
from flask_wtf.html5 import EmailField
from wtforms.validators import DataRequired, Email
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from .util.validators import Unique
from .models import User, FieldType
from wtforms.widgets import HiddenInput


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

class SearchInterfaceForm(Form):
    fieldname = StringField('fieldname', validators=[DataRequired()])
    description = StringField('description')
    header = SelectMultipleField(label='header')
    display = SelectField(label='display', choices = [(name, member.value) for name, member in FieldType.__members__.items()])

    def __init__(self, headers):
        super(SearchInterfaceForm, self).__init__()
        self.header.choices = headers

class SearchField(Form):
    # Need to add validators when javascript for adding rows is implemented
    fieldname = StringField()
    field_description = StringField()
    header = SelectMultipleField()
    field_type = SelectField(choices = [(name, member.value) for name, member in FieldType.__members__.items()])

class SearchInterface(Form):
    # Need to change min_entries to 1 when javascript for adding rows is implemented
    search_fields = FieldList(FormField(SearchField), min_entries=5)
    # full_text_search = BooleanField(label="Full text search on collection")
    full_text_search = BooleanField()

class TextboxForm(Form):
    search_field_id = IntegerField(widget=HiddenInput())
    search = StringField()

class UniqueSearchForm(Form):
    search_field_id = IntegerField(widget=HiddenInput())
    search = SelectField('search')
    # 
    # def set_default(self, value):
    #     self.search.default = 'value'

class DisplayForm(Form):
    text_searches = FieldList(FormField(TextboxForm))
    unique_searches = FieldList(FormField(UniqueSearchForm))
