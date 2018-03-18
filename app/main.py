from flask import Flask, redirect, url_for, request, jsonify, render_template, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_cors import CORS
from datetime import datetime
import json
import re
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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

db.create_all()

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/create', methods=('GET', 'POST'))
def admin_create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        keywords = request.form['keywords']
        stages = request.form['stages']
        current_no_stage = 0
        status = request.form['status']
        document = request.files['document']
        total_no_stages = len(stages.split(","))

        print (request.form)

        # generate a unique filename

        extension = str(datetime.now)
        extension = '-'.join(extension.split())
        filename = '{}-{}'.format(document.filename, extension)

        print (filenameg)

        document.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        doc = Document(filename, title, description, keywords, total_no_stages, stages, current_no_stage, status)
        db.session.add(doc)
        db.session.commit()

        return redirect(url_for('admin'))
    else:
        return render_template('admin-create.html')

@app.route('/admin/edit/<int:doc_id>', methods=('GET', 'POST'))
def admin_edit(doc_id):
    if request.method == 'GET':
        document = Document.query.filter_by(id=doc_id).all()[0]
        return render_template('admin-edit.html', docs=document)
    else:
        title = request.form['title']
        description = request.form['description']
        keywords = request.form['keywords']
        total_no_stages = int(request.form['total_no_stages'])
        stages = int(request.form['stages'])
        current_no_stage = int(request.form['current_no_stages'])
        status = int(request.form['status'])
        document = request.files['document']

        doc = Document.query.filter_by(id=doc_id).all()[0]
        doc.title = title
        doc.description = description
        doc.keywords = keywords
        doc.total_no_stages = total_no_stages
        doc.stages = stages
        doc.current_no_stage = current_no_stage
        doc.status = status

        if document:
            extension = str(datetime.now)
            extension = '-'.join(extension.split())
            new_filename = '{}-{}'.format(document.filename, extension)
            os.unlink(os.path.join(app.config['UPLOAD_FOLDER'], doc.filename))
            document.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
            doc.filename = new_filename

        db.session.commit()

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        query = request.form['query']
        query = query.lower()
        query_tokens = query.split()
        docs = Document.query.all()
        user_docs = []
        
        for doc in docs:
            doc_keywords = doc.keywords.split(',')
            doc_keywords = set([doc_keyword.trim() for doc_keyword in doc_keywords])
            common = len(doc_keywords.intersection(set(query_tokens)))
            if common != 0:
                user_docs.append({'doc': doc, 'score':common})
        user_docs.sort(key=lambda x:x['score'], reverse=True)
        user_docs = [user_doc['soc'] for user_doc in user_docs]
        return render_template('index.html', docs=user_docs)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
