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
from sqlalchemy import engine, text, union, select, String, and_
from sqlalchemy.sql import table, literal_column
from .forms import SignupForm, LoginForm, SearchInterfaceForm, SearchInterface, TextboxForm, UniqueSearchForm, DisplayForm
from .util.security import ts
from flask_login import login_user, logout_user, login_required
from flask.ext.login import current_user
from collections import OrderedDict
from flask.ext.wtf import Form


@app.route('/')
def index():
    return redirect('/main')


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
    return render_template("createUpload.html")


# API endpoint to store in db the file a user has selected
@app.route("/storeFile", methods=["POST"])
@login_required
def saveFile():
    print("Storing file")
    # Need to do some error checking on file
    file_url = request.form["url"]
    file_id = file_url.split('/')[-1]

    # Get file from filestack, Might need to implement HTTPS
    httpResponse = urlopen(file_url + "/metadata")
    print("The server's response to {} was {}".format(file_url, httpResponse.status))
    file_metadata = json.loads(httpResponse.read().decode("utf-8"))
    mimetype = file_metadata["mimetype"]

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
        db.session.commit()

        # Add search interface id to session to access si
        session['search_interface_id'] = si.id
        print("The search interface saved under id {}".format(session['search_interface_id']))

        # Create document and link it to the search interface
        document = models.Document()
        document.document_id = file_id
        document.search_interface = si.id

        # Create headers and link them to the document
        query_result = db.engine.execute('PRAGMA table_info("{}")'.format(document.document_id)).fetchall()
        for item in query_result:
            header = models.Header()
            header.header_name = item[1]
            header.document = document.document_id
            db.session.add(header)

        db.session.add(user)
        db.session.add(document)
        db.session.commit()

    else:
        # COMPLETE check if file has been updated and passes test than can add file
        pass

    return jsonify(validation)

@app.route("/createSearch", methods=['GET', 'POST'])
def createSearch():
    print("-----Entered create search interface-----")
    si_id = session["search_interface_id"]
    document = models.Document.query.filter_by(search_interface=si_id).first()
    headers = models.Header.query.filter_by(document=document.document_id).all()
    headers_names = [(header.header_name, header.header_name) for header in headers] # Headers is a list of header names

    ## Initialising SearchInterface form, could be done in object
    print("The submitted form data is:\n{}".format(request.form))
    searchform = SearchInterface(request.form) # Bug in Flask-WTF with dynamic form, need to use original WTF
    for search_field in searchform.search_fields:
        search_field.header.choices = headers_names

    # print("---- Submitted form: \n{}".format(request.form))
    # for search_fields in searchform.search_fields:
    #     for search_field in search_fields:
    #         print("{}, {}".format(search_field.label, search_field.validate(searchform)))
    if request.method == 'POST' and searchform.validate():
        # Process full_text_search
        if searchform.full_text_search.data:
            print("Adding full text search")
            searchfield = models.SearchField(
                name = "Full text search",
                description = "",
                field_type = models.FieldType.Textbox.name,
                search_interface = si.id ## To be changed when suporting multiple SI
            )
            for header in headers:
                searchfield.headers.append(header)
            db.session.add(searchfield)

        # Process custom search fields
        for search_field in searchform.search_fields:
            print("------------Saving search field {} to db -------------".format(search_field.data))

            ## To be removed when form validation is implemented
            if not search_field.fieldname.data or not search_field.header.data:
                print("------Incomplete search field, not saved-----")
                continue;
            ##

            # Add search_field to db
            searchfield = models.SearchField(
                name = search_field.fieldname.data,
                description = search_field.field_description.data,
                field_type = search_field.field_type.data
            )
            searchfield.search_interface = si.id

            # Add headers selected to db
            for header_name in search_field.header.data:
                header = models.Header.query \
                    .filter_by(header_name=header_name) \
                    .filter_by(document=document.document_id) \
                    .first()
                searchfield.headers.append(header)
                print('Added header {}'.format(header_name))

            db.session.add(searchfield)
            db.session.commit()

        return redirect(url_for("search"))

    return render_template("createSearchSimple.html", form=searchform)


@app.route("/interface")
def interface():
    return render_template("interface.html")


# Page to actually search the database
# Need to implement custom URL to serve individual search interface
@app.route("/search", methods=['GET', 'POST'])
def search():
    ## Getting all the required information to conduct queries
    si_id = session["search_interface_id"]
    document = models.Document.query.filter_by(search_interface=si_id).first()
    search_fields = models.SearchField.query.filter_by(search_interface=si_id).all()

    #Instantiate Displayform so we can insert textboxform or dropdown form
    displayform = DisplayForm()
    for field in search_fields:
        if(field.field_type == "Textbox"):
            displayform.text_searches.append_entry()
            textboxform = displayform.text_searches.entries[-1]
            textboxform.search_field_id.default = field.id
            textboxform.search.label = str(field.name)
        else:
            #Querying the selected headers for a given header
            selected_header = models.Header.query.filter(models.Header.search_fields.any(id=field.id)).all()
            # getting the table to query the content inside a header
            document_model = document.document_id
            choice = []
            # for every header
            for head in selected_header:
                sql = text("SELECT DISTINCT " + str(head.header_name) + " FROM \"" + str(document_model) + "\"") #querying the db
                result = db.engine.execute(sql)
                for item in result:
                    choice.append((str(item[0]),str(item[0])))

            displayform.unique_searches.append_entry()
            uniquesearchform = displayform.unique_searches.entries[-1]
            uniquesearchform.search.label = str(field.name)
            uniquesearchform.search.choices = choice
            uniquesearchform.search_field_id.default = field.id

    if request.method == 'POST':
        print('############################submitting the form############################')
        text_queries = []
        unique_queries = []
        unique_headers = []
        text_headers = []

        for field in displayform.text_searches:
            print('adding the text search')
            text_queries.append(field.search.data)
            text_headers.append(field.search_field_id.default)
            print(field.search_field_id.default)
        for field in displayform.unique_searches:
            print('adding the unique search')
            unique_queries.append(field.search.data)
            unique_headers.append(field.search_field_id.default)

        text_queries = [x for x in text_queries if x is not 'None' and x is not None]
        text_headers = [x for x in text_headers if x is not 'None' and x is not None]
        unique_queries = [x for x in unique_queries if x is not 'None' and x is not None]
        unique_headers = [x for x in unique_headers if x is not 'None' and x is not None]

        print('printing text queries')
        print(text_queries)
        print('printing text headers')
        print(text_headers)

        for query in text_queries:
            i = 0
            if query != 'None' and query != None:
                print('printing text headers')
                print(text_headers)
                selected_header = models.Header.query.filter(models.Header.search_fields.any(id=text_headers[i])).all()
                print('print selected header')
                print(selected_header[i].header_name)

                # print('printing query')
                # query = query.split(' ')
                # print(query)
                # sql_query = []
                # if len(query) > 1:
                #     index = 0
                #     for q in query:
                #         if index < (len(query) - 1):
                #             sql_query.append("'%" + str(q) + "%' OR " + str(selected_header[i].header_name) + " LIKE ")
                #             index += 1
                # print('printing sql_query')
                # print(sql_query)
                sql_text = str("SELECT * FROM " + str(document_model) + " WHERE " + str(selected_header[i].header_name) + " LIKE '%" + str(query) + "%' INTERSECT ") #querying the d

                # sql = text("SELECT * FROM " + str(document_model) + " WHERE " + str(selected_header[i].header_name) + " LIKE '%" + str(query) + "%'") #querying the d
                # sql = select([str(document_model)]).where(literal_column(selected_header[i].header_name).like(query))
                result = db.engine.execute(sql)
                i += 1

        for query in unique_queries:
            i = 0
            if query != 'None' and query != None:
                print(query)
                print('printing unique headers')
                print(unique_headers)
                selected_header = models.Header.query.filter(models.Header.search_fields.any(id=unique_headers[i])).all()
                print(selected_header)
                sql_unique = str("SELECT * FROM " + str(document_model) + " WHERE " + str(selected_header[i].header_name) + " = '" + str(query) + "';") #querying the db

                # sql_unique = text("SELECT * FROM " + str(document_model) + " WHERE " + str(selected_header[i].header_name) + " = '" + str(query) + "';") #querying the db

                # unique_sql = text("SELECT * FROM " + str(document_model) + " WHERE " + str(selected_header[i].header_name) + " = '" + str(query) + "';") #querying the db
                # unique_result = db.engine.execute(sql)
                i += 1

        sql = text(sql_text + sql_unique)
        print(sql)
        result = db.engine.execute(sql)

        data = []
        for v in result:
            d = OrderedDict([])
            for column, value in v.items():
                d[str(column)] = str(value)
                #print('{0}: {1}'.format(column, value))
            data.append(d)
        return json.dumps(data)
        return redirect(url_for("search"))
        # return json.dumps(data)
    return render_template("search.html", form=displayform)

@app.route("/updateData", methods=["GET"])
@login_required
def updateData():
    json = escape(session['json']) #getting the name of the table
    return json.dumps(data)

@app.route("/getData", methods=["GET"])
@login_required
def getData():
    print("----Getting data-----")
    document = models.Document.query.filter_by(search_interface=session['search_interface_id']).first()
    document_id = escape(document.document_id)
    sql = text("SELECT * FROM \"" + str(document_id) + "\"") #querying the db
    result = db.engine.execute(sql)

    data = []
    for v in result:
        d = OrderedDict([])
        for column, value in v.items():
            d[str(column)] = str(value)
            #print('{0}: {1}'.format(column, value))
        data.append(d)
    return json.dumps(data)

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/profile")
def projects():
    return render_template("profile.html")

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
