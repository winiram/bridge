from flask import render_template, redirect, request, flash, jsonify, url_for, g, escape, session
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
from .forms import SignupForm, LoginForm
from .util.security import ts
from flask_login import login_user, logout_user, login_required
from flask.ext.login import current_user

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
    # Temporarily just create one search interface
    if not models.SearchInterface.query.first():
        user = models.User.query.first()
        si = models.SearchInterface()
        user.search_interfaces.append(si)
        db.session.add(user)
        db.session.commit()
    return render_template("createUpload.html")

@app.route("/previewUpload", methods=['POST'])
@login_required
def previewUpload():
    global test_file_url
    si = models.SearchInterface.query.first()
    file_url = 'https://www.filestackapi.com/api/file/' + si.document_id;
    return render_template("previewUpload.html", url=file_url)

@app.route("/storeFile", methods=["POST"])
@login_required
def saveFile():
    print("Storing file")
    # Need to do some error checking on file
    file_url = request.form["url"]
    # file_url = 'https://www.filestackapi.com/api/file/QROhdz5ITLOHRKP1mBlr'
    file_id = file_url.split('/')[-1]

    # Get file from filestack, Might need to implement HTTPS
    httpResponse = urllib.request.urlopen(file_url + "/metadata")
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
        df.to_sql(file_id, db.engine, index=False)
        si = models.SearchInterface.query.first() # REPLACE WITH SI ID IN SESSION
        si.document_id = file_id
        db.session.commit()
    else:
        # COMPLETE check if file has been updated and passes test than can add file
        pass

    return jsonify(validation)

@app.route("/createSearch")
def createSearch():
    return render_template("createSearch.html")

@app.route("/previewSearch")
@login_required
def previewSearch():
    return render_template("previewSearch.html")

<<<<<<< HEAD
@app.route("/interface")
def searchInterface():
    return render_template("interface.html")

@app.route("/search")
def searchInterface_side():
    return render_template("search.html")        


@app.route("/test")
def test():
    return render_template("test.html")   
=======
@app.route("/searchInterface")
@login_required
def searchInterface():
    return render_template("searchInterface.html")

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
>>>>>>> master
