import directory
import re
import random
import logging
from logging.handlers import RotatingFileHandler
import os
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, render_template, request, escape, flash, redirect, request, session, abort, url_for, json
from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField, TextAreaField
import datetime, time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc


app = Flask(__name__, static_folder='static/assets')
app.config['DEBUG'] = True

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
COLUMN_LIMITS = {
    'fname'     : 64,
    'lname'     : 64,
    'email'     : 64,
    'grade'     : 32,
    'school'    : 64,
    'busorigin' : 80,
    'website'   : 80,
    'linkedin'  : 80,
    'resumepath': 120,
    'major'     : 80
}

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
class RegistrationForm(Form):
    fname = StringField('First Name', [validators.Length(min=1, max=COLUMN_LIMITS['fname']), validators.DataRequired()])
    lname = StringField('Last Name', [validators.Length(min=1, max=COLUMN_LIMITS['lname']), validators.DataRequired()])
    email = StringField('Email', [validators.Length(min=6, max=COLUMN_LIMITS['email']), validators.Email(), validators.DataRequired()])
    age = BooleanField('Age')
    grade = StringField('Grade', [validators.Length(max=COLUMN_LIMITS['grade']), validators.DataRequired()])
    school = StringField('School/University', [validators.Length(max=COLUMN_LIMITS['school']), validators.DataRequired()])
    major = StringField('Major', [validators.Length(max=COLUMN_LIMITS['major']), validators.DataRequired()])
    busorigin = StringField('Bus Origin')
    webdev = BooleanField('Web Development')
    mobiledev = BooleanField('Mobile Development')
    arvrdev = BooleanField('AR/VR Development')
    hardwaredev = BooleanField('Hardware Development')
    aidev = BooleanField('AI Development')
    website = StringField('Website', [validators.Length(max=COLUMN_LIMITS['website'])])
    linkedin = StringField('LinkedIn Profile', [validators.Length(max=COLUMN_LIMITS['linkedin'])])
    poem = TextAreaField('Question 1: Poem')
    techsimplify = TextAreaField('Question 2: Simplify Something With Technology')
    hacktechsuggest = TextAreaField('Question 3: Suggestions for Hacktech')
    othercomment = TextAreaField('Question 4: Questions/Comments/Concerns')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])



@app.route('/leaderboard')
def leaderboard(name=None):
    name = request.args["name"]
    return render_template('leaderboard.html', name=name, game_name=directory.GAME_NAME_LIST, game_desc=directory.GAME_DESCRIPTION_LIST, game_link=directory.GAME_LINK_LIST)

def check(code, inp, outp):
    try:
        exec(code)
    except:
        return ('Syntax error! Try again!', 0)
    for test_case in range(len(inp)):
        try:
            result = eval('f(' + str(inp[test_case]) + ')')
            if result != outp[test_case]:
                return ("Wrong Answer! Try again!", 0)
        except:
            return ("Function error! Try again!", 0)
    return ("You passed with %d characters" %(len(code)), len(code))

@app.route('/api/code_golf', methods=['GET', 'POST'])
def golf():
    if request.method == 'POST':
        content = request.form["code"]
        question = request.form["question"]
        inp = directory.CODE_GOLF_ANSWERS_LIST[question]["inputs"]
        outp = directory.CODE_GOLF_ANSWERS_LIST[question]["outputs"]
        result, length = check(content, inp, outp)
        return json.dumps({"result": result, "chars": length})
    elif request.method == 'GET':
        return json.dumps(directory.CODE_GOLF_QUESTIONS_LIST)
    return "no"

@app.route('/api/movepaths')
def save_user():
        username = request.args["username"]
        return redirect(url_for('leaderboard', name=username))


@app.route('/api/passwordgen', methods=['GET'])
def password_generation():
    if request.method == 'GET':
        pwd = ""
        pwd += random.choice(directory.COMMON_WORD_LIST_NOUN)
        pwd += random.choice(directory.COMMON_WORD_LIST_VERB)
        pwd += random.choice(directory.COMMON_WORD_LIST_NOUN)
        pwd += random.choice(directory.COMMON_NUMBER_LIST)
        return pwd

@app.route('/api/trivia_game', methods=['GET', 'POST'])
def trivia():
    # GET pulls the next question in line in TRIVIA_QUESTIONS_LIST
    if request.method == 'GET':
        key = int(request.args.get('question'))
        if key in directory.TRIVIA_QUESTIONS_LIST:
            return directory.TRIVIA_QUESTIONS_LIST[key]
        else:
            return "No questions left! Check back later for more!"
    # POST normalizes the user and database answers and compares them
    elif request.method == 'POST':
        answer = request.form["answer"]
        questionNum = int(request.form["question"])
        if (normalize(directory.TRIVIA_ANSWERS_LIST[questionNum]) == \
            normalize(answer)):
            return json.dumps({"result": "Correct!"})
        return json.dumps({"result": "Wrong! Correct Answer: %s" \
                           %(directory.TRIVIA_ANSWERS_LIST[questionNum])})
    return "Wrong request method given."

def normalize(string):
    return re.sub(r'\W+', '', string.lower())

@app.route('/play/<gamename>')
def play_game(gamename, username=None):
    username = request.args.get('username')
    if gamename is None or username is None:
        return redirect(url_for('login'))
    return render_template('games/%s.html' % gamename, username=username)

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] in directory.USER_TO_PASS_LIST.keys():
            if request.form['password'] == directory.USER_TO_PASS_LIST[request.form['username']]:
                return redirect(url_for('leaderboard', name=request.form['username']))
            error = 'Invalid Credentials. Please try again.'
        error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

if __name__ == "__main__":
    app.run()
