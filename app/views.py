from flask import *
from flask_login import current_user, login_required, login_user, logout_user
from app import app
from .forms import *
from .helpers.dbHelper import DbHelper
import bcrypt

@app.before_request
def set_role():
    user = DbHelper.get_user_by_id(current_user.get_id())
    if user != None:
        if int(user.account_type) == UserType.USER.value:
            g.role = "user"
        elif int(user.account_type) == UserType.MANAGER.value:
            g.role = "manager"

@app.route("/")
def index():
    user = DbHelper.get_user_by_id(current_user.get_id())

    if user == None:
        return redirect(url_for("login"))

    if (int(user.account_type) == UserType.USER.value):
        return redirect(url_for("user.home"))
    elif (int(user.account_type) == UserType.MANAGER.value):
        return redirect(url_for("manager.home"))
    else:
        return redirect(url_for("logout"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        result = DbHelper.create_user(form.email.data, 
                             form.fname.data, 
                             form.lname.data,
                             form.account_type.data,
                             form.password.data)
        if result != None:
            flash("Successfully created your account! Please login.")
            return redirect(url_for("login"))
        else:
            flash("There was an error creating your account!")
        
    return render_template("auth_pages/signup_page.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        result = DbHelper.get_user_by_email(form.email.data)
        if result == None:
            flash("Invalid email or password.")
            return redirect(url_for("login"))
        correct_pwd = bcrypt.checkpw(bytes(form.password.data, "utf-8"), result.password_hash)
        if correct_pwd != True:
            flash("Invalid email or password.")
            return redirect(url_for("login"))
        login_res = login_user(result)
        if login_res != True:
            flash("Invalid email or password.")
            return redirect(url_for("login"))
        
        result.is_authenticated = True
        DbHelper.update_user(result.id, result)
        
        if (int(result.account_type) == UserType.USER.value):
            return redirect(url_for("user.home"))
        else:
            return redirect(url_for("manager.home"))
        
    return render_template("auth_pages/login_page.html", form=form)

@app.route("/logout")
@login_required
def logout():
    current_user.is_authenticated = False
    DbHelper.update_user(current_user.id, current_user)
    logout_user()
    return redirect(url_for("login"))

@app.route("/account", methods=["GET", "POST"])
@login_required
def account_settings():
    user = DbHelper.get_user_by_id(current_user.get_id())
    if user == None:
        return redirect(url_for("error_404"))
    form = AccountSettingsForm()

    if form.validate_on_submit():
        user.email = form.email.data
        user.fname = form.fname.data
        user.lname = form.lname.data
        if (form.password.data):
            user.password_hash = bcrypt.hashpw(bytes(form.password.data, "utf-8"), bcrypt.gensalt(rounds=12))
        result = DbHelper.update_user(user.id, user)
        if result == None:
            flash("Error updating your account!", "danger")
        else:
            flash("Successfully updated your account!", "success")
    else:
        form.email.data = user.email
        form.fname.data = user.fname
        form.lname.data = user.lname

    return render_template("account_settings.html",
                           form=form,
                           page_title="Account Settings")
    
@app.route("/404")
@login_required
def error_404():
    return render_template("404.html",
                           page_title="ERROR 404")

@app.route("/500")
@login_required
def error_500():
    return render_template("500.html",
                           page_title="ERROR 500")