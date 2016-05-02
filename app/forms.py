from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, PasswordField, FieldList, SelectField, SelectMultipleField, FormField, FieldList, BooleanField
from wtforms import Form as WTForm
from flask_wtf.html5 import EmailField
from wtforms.validators import DataRequired, Email, Optional
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

##### Search creation forms ####
# Bug in Flask-WTF with dynamic form, need to use original WTF
class SearchField(WTForm):
    # Need to add validators when javascript for adding rows is implemented
    fieldname = StringField()
    field_description = StringField()
    header = SelectMultipleField()
    field_type = SelectField(choices = [(name, member.value) for name, member in FieldType.__members__.items()], default = "Textbox")

class SearchInterface(WTForm):
    search_fields = FieldList(FormField(SearchField), min_entries=1)
    full_text_search = BooleanField()


##### Search forms ####
class TextboxForm(Form):
    search_field_id = IntegerField(widget=HiddenInput())
    search = StringField()

class UniqueSearchForm(Form):
    search_field_id = IntegerField(widget=HiddenInput())
    search = SelectField(coerce=str, validators=[Optional()])

class DisplayForm(Form):
    text_searches = FieldList(FormField(TextboxForm))
    unique_searches = FieldList(FormField(UniqueSearchForm))
