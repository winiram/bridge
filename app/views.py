from flask import render_template, redirect, request, flash, jsonify, url_for, g, escape, session, render_template_string
from app import app, models, db, fileprocessing
import base64, json, time
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
import pandas as pd
from sqlalchemy import engine
from .forms import SignupForm, LoginForm, SearchInterfaceForm, SearchInterface
from .util.security import ts
from flask_login import login_user, logout_user, login_required
from flask.ext.login import current_user


@app.route('/')
def index():
    return redirect('/main')

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route("/main")
def main():
    email = ''
    if 'email' in session:
        email = escape(session['email'])
        return render_template("main.html", email=email)
    else:
        return render_template('main.html')

@app.route("/createUpload")
@login_required
def createUpload():
    # # Temporarily just create one search interface
    # if not models.SearchInterface.query.first():
    #     user = models.User.query.first()
    #     si = models.SearchInterface()
    #     user.search_interfaces.append(si)
    #     db.session.add(user)
    #     db.session.commit()
    return render_template("createUpload.html")

@app.route("/storeFile", methods=["POST"])
@login_required
def saveFile():
    print("Storing file")
    # Need to do some error checking on file
    file_url = request.form["url"]
    # file_url = 'https://www.filestackapi.com/api/file/QROhdz5ITLOHRKP1mBlr'
    file_id = file_url.split('/')[-1]

    # Get file from filestack, Might need to implement HTTPS
    httpResponse = urlopen(file_url + "/metadata")
    print("The server's response to {} was {}".format(file_url, httpResponse.status))
    file_metadata = json.loads(httpResponse.read().decode("utf-8"))
    mimetype = file_metadata["mimetype"]
    print(mimetype)

    # Check for valid file, if it contains headers.
    df = fileprocessing.load(file_url, mimetype)
    validation = fileprocessing.validate(df)
    if not validation["success"]:
        return jsonify(validation)

    # If file is valid store in database, otherwise return to upload page with error message
    if not db.engine.has_table(file_id):
        # Create table on the fly
        df.to_sql(file_id, db.engine, index=False)

        user = models.User.query.filter_by(email=session["email"]).first()

        # Create search interface and link it to the user
        si = models.SearchInterface(user = user.id)
        db.session.add(si)

        # Create document and link it to the search interface
        si_query = models.SearchInterface.query.filter_by(user=user.id).first()
        print("printing search interface id: {}".format(si_query.id))

        document = models.Document()
        document.document_id = file_id
        document.search_interface = si_query.id

        # Create headers and link them to the document
        query_result = db.engine.execute('PRAGMA table_info("{}")'.format(document.document_id)).fetchall()
        # Headers is a list of (header_name, header_value)
        for item in query_result:
            print(item)
            header = models.Header()
            header.header_name = item[1]
            header.document = document.document_id
            db.session.add(header)

        db.session.add(user)
        # db.session.add(si)
        db.session.add(document)
        db.session.commit()
    else:
        # COMPLETE check if file has been updated and passes test than can add file
        pass

    return jsonify(validation)

@app.route("/createSearch", methods=['GET', 'POST'])
def createSearch():
    user = models.User.query.filter_by(email=session["email"]).first()
    si = models.SearchInterface.query.filter_by(user=user.id).first() #assuming user has only one search interface
    document = models.Document.query.filter_by(search_interface=si.id).first()
    headers = models.Header.query.filter_by(document=document.document_id).all()
    headers_names = [(header.header_name, header.header_name) for header in headers] # Headers is a list of header names

    searchform = SearchInterface()
    for search_field in searchform.search_fields:
        search_field.header.choices = headers_names

    print(request.form)
    if request.method == 'POST' and searchform.validate_on_submit():
        for search_field in searchform.search_fields:
            print("------------printing search field data -------------")
            print(search_field.data)
            ## To be removed when form validation is implemented
            if not search_field.fieldname.data or not search_field.header.data:
                print("------Incomplete search field, not saved-----")
                continue;
            ##
            # Add search_field to db
            searchfield = models.SearchField(
                name = search_field.fieldname.data,
                description = search_field.field_description.data,
                field_type = search_field.field_type.data,
            )

            # Add headers selected to db
            for header_name in search_field.header.data:
                header = models.Header.query \
                    .filter_by(header_name=header_name) \
                    .filter_by(document=document.document_id) \
                    .first()
                searchfield.headers.append(header)

            db.session.add(searchfield)
            db.session.commit()
        return redirect(url_for("interface"))

        # if "action" not in request.form and searchform.validate_on_submit():
        # elif request.form["action"] == "add":
        #     print("Adding row requested")
        #     searchform.search_fields.append_entry()
        #     searchform.search_fields.entries[-1].header.choices = headers_names
        # elif request.form["action"] == "remove":
        #     pass

    return render_template("createSearchSimple.html", form=searchform)

@app.route("/previewSearch")
@login_required
def previewSearch():
    return render_template("previewSearch.html")


@app.route("/interface")
def interface():
    return render_template("interface.html")

@app.route("/search")
def searchInterface_side():
    return render_template("search.html")


@app.route("/test")
def test():
    return render_template("test.html")


@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    signupform = SignupForm()
    if signupform.validate_on_submit():
        user = models.User(
            fname = signupform.fname.data,
            lname = signupform.lname.data,
            email = signupform.email.data,
            password = signupform.password.data
        )
        session['email'] = signupform.email.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('log_in'))
    return render_template("signup.html", form=signupform)

@app.route('/log_in', methods=["GET", "POST"])
def log_in():
    email = ''
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    loginform = LoginForm()
    if request.method == 'POST' and loginform.validate_on_submit():
        user = models.User.query.filter_by(email=loginform.email.data).first_or_404()
        if user.is_correct_password(loginform.password.data):
            login_user(user)
            session['email'] = loginform.email.data
            flash("You are now logged in", 'success')
            email = session['email']
            return render_template("main.html", email=email)
        else:
            flash('Username and password do not match', 'error')
    return render_template('login.html', form=loginform)

@app.route('/log_out')
def log_out():
    session.pop('username', None)
    session.pop('email', None)
    logout_user()
    return redirect(url_for('main'))

@app.before_request
def before_request():
    g.user = current_user
