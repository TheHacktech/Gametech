import logging
from logging.handlers import RotatingFileHandler
import os
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, render_template, request, escape
from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField, TextAreaField
import datetime, time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

from utils.email_client import send_email

app = Flask(__name__, static_folder='static/assets')

# get the logger working
if not app.debug:
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
    logFile = 'server.log'
    my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=1*1024*1024,
                                     backupCount=2, encoding=None, delay=0)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.INFO)
    app.logger.addHandler(my_handler)

# logging.basicConfig(filename='email_client.log',level=logging.DEBUG,
#                     format='%(asctime)s %(message)s')

# application configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hacktech'
app.config['UPLOAD_FOLDER'] = '/home/potato/resumes'

# constants
ALLOWED_EXTENSIONS = set(['doc', 'docx', 'pdf', 'txt', 'rtf'])

# models #######################################################################

db = SQLAlchemy(app)

# dict of max length of each column in the db


class Hacker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(COLUMN_LIMITS['fname']))
    lname = db.Column(db.String(COLUMN_LIMITS['lname']))
    email = db.Column(db.String(COLUMN_LIMITS['email']), unique=True)
    age = db.Column(db.Boolean)
    grade = db.Column(db.String(COLUMN_LIMITS['grade']))
    school = db.Column(db.String(COLUMN_LIMITS['school']))
    busorigin = db.Column(db.String(COLUMN_LIMITS['busorigin']))
    webdev = db.Column(db.Boolean)
    mobiledev = db.Column(db.Boolean)
    arvrdev = db.Column(db.Boolean)
    hardwaredev = db.Column(db.Boolean)
    aidev = db.Column(db.Boolean)
    website = db.Column(db.String(COLUMN_LIMITS['website']))
    linkedin = db.Column(db.String(COLUMN_LIMITS['linkedin']))
    poem = db.Column(db.Text)
    techsimplify = db.Column(db.Text)
    hacktechsuggest = db.Column(db.Text)
    othercomment = db.Column(db.Text)
    accept_tos = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime)
    resumepath = db.Column(db.String(COLUMN_LIMITS['resumepath']))
    major = db.Column(db.String(COLUMN_LIMITS['major']))

    def __init__(self, fname, lname, email, age, grade, school, busorigin, webdev, mobiledev, arvrdev, hardwaredev, aidev, website, linkedin, poem, techsimplify, hacktechsuggest, othercomment, accept_tos, timestamp, resumepath, major):
        '''
        initialize the user database.
        things that should be stored:
        first name, last name, school, grade
        transportation, which bus if any
        interested in: web dev, mobile dev, AR/VR, hardware, AI/ML, other
        resume file
        links to github, linkedin, portfolio
        over 18 by march 3, 2017?
        acrostic poem based around the word "ROSE"
        something you did today that could have been enhanced by tech
        cool things you'd like to see at hacktech
        questions/comments/concerns
        do you accept MLH code of conduct?
        '''
        self.fname           = fname
        self.lname           = lname
        self.email           = email
        self.age             = age
        self.grade           = grade
        self.school          = school
        self.busorigin       = busorigin
        self.webdev          = webdev
        self.mobiledev       = mobiledev
        self.arvrdev         = arvrdev
        self.hardwaredev     = hardwaredev
        self.aidev           = aidev
        self.website         = website
        self.linkedin        = linkedin
        self.poem            = poem
        self.techsimplify    = techsimplify
        self.hacktechsuggest = hacktechsuggest
        self.othercomment    = othercomment
        self.accept_tos      = accept_tos
        self.timestamp       = timestamp
        self.resumepath      = resumepath
        self.major           = major

    def __repr__(self):
        return self.fname + ' ' + self.lname + ' ' + self.email + ' ' + str(self.age) + ' ' + self.grade + ' ' + self.school + ' ' + self.busorigin + ' ' + str(self.webdev) + ' ' + str(self.mobiledev) + ' ' + str(self.arvrdev) + ' ' + str(self.hardwaredev) + ' ' + str(self.aidev) + ' ' + self.website + ' ' + self.linkedin + ' ' + self.poem + ' ' + self.techsimplify + ' ' + self.hacktechsuggest + ' ' + self.othercomment + ' ' + str(self.accept_tos) + ' ' + str(self.timestamp) + ' ' + self.resumepath + ' ' + self.major













# DONT PUSH






db.create_all()
db.session.commit()











# forms ########################################################################

# Registration form needed for backend validation
