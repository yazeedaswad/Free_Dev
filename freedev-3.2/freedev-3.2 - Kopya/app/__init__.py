#this file sets up the database, and the models.py file creates tables for this database

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, instance_relative_config = True)
app.config["SECRET_KEY"] =  '666AAA'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///freelancer_employer_information.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

app.config.from_object('config')

from app import views
from app import models 



