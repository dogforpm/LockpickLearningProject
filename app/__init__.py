# Imports
from flask import Flask, render_template, request, redirect, url_for
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Define app to allow as import
app = Flask(__name__)
# Run app configeration
app.config.from_object(Config)
# Define database to allow as import
db = SQLAlchemy(app)
# Define migrate to allow as import
migrate = Migrate(app, db)
# Define loginManager to allow as import
login = LoginManager(app)

from app import routes, models