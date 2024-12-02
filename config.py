import os

# WTF Forms
WTF_CSRF_ENABLED = True
SECRET_KEY = "a17G+mZ*!GE[.^w8"

# Database Config
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "shift-schedule-db.db")
SQLALCHEMY_TRACK_MODIFICATIONS = True
