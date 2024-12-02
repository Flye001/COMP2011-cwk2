from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .user.views import user_bp
from .manager.views import manager_bp
from app.db import db

app = Flask(__name__)
app.config.from_object("config")
app.secret_key = "a17G+mZ*!GE[.^w8"

db.init_app(app)
Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Session configuration (adjust for production)
app.config["SESSION_COOKIE_SECURE"] = False  # True for HTTPS in production
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=7)

app.register_blueprint(user_bp)
app.register_blueprint(manager_bp)

from app import views, models
from .helpers.dbHelper import DbHelper

@login_manager.user_loader
def load_user(user_id):
    user = DbHelper.get_user_by_id(user_id)
    return user