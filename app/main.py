from flask import Flask, redirect, url_for, request, jsonify, render_template, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_cors import CORS
import json
import re
import os

app = Flask(__name__)
CORS(app)
if os.environ.get('DATABASE_URL') is None:
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///versions.sqlite3'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/deep'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SECRET_KEY'] = "THIS IS SECRET"

db = SQLAlchemy(app)

class Document(db.Model):
    __tablename__ = 'Document'

    id = db.Column('document_id', db.Integer, primary_key=True)
    filename = db.Column(db.String)
    title = db.Column(db.String)
    description = db.Column(db.String)
    keywords = db.Column(db.String)
    total_no_stages = db.Column(db.Integer)
    stages = db.Column(db.String)
    current_no_stage = db.Column(db.Integer)
    status = db.Column(db.String)


    def __init__(self, filename='', title='', description='', keywords='', total_no_stages='', stages='', current_no_stage='', status=''):
        self.filename=filename
        self.title = title
        self.description = description
        self.keywords = keywords
        self.total_no_stages = total_no_stages
        self.stages = stages
        self.current_no_stage = current_no_stage
        self.status = status

class Users(db.Model):
    __tablename__ = 'Users'

    id = db.Column('user_id', db.Integer, primary_key=True)
    email = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    password = db.Column(db.String)
    designation = db.Column(db.String)

    def __init__(self, email='', first_name='', last_name='', password='', designation=''):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.designation = designation

    def __repr__(self):
        return '<User %r>' % self.email
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.email)

@app.route('/')
def index():
    return ('hellow world')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
