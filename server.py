from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, json
import directory
import re
import random
import multiprocessing

app = Flask(__name__, static_folder='static/assets')
# app = Flask(__name__)
app.config['DEBUG'] = True

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
	    # Creating a child process that can be terminated after a time limit
	    p = multiprocessing.Process(target=f, name="F", args=(test_case,))
	    p.start()

	    # Wait a maximum of 5 seconds for foo
	    # Usage: join([timeout in seconds])
	    p.join(3)

	    # If thread is active
	    if p.is_alive():
		# Terminate function
		p.terminate()
		p.join()
		return ("Function is taking too long! Try again!", 0)

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

@app.route('/gametech', methods=['GET', 'POST'])
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

@app.route('/')
def index():
    return render_template('JoinTechTemplates/index.html')

@app.route('/waiver/')
def waiver():
    return render_template('JoinTechTemplates/waiver.html')

@app.route('/apply/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():

        buses = ["no", "tech", "stan", "ucb", "uci", "ucla", "ucsd", "usc"]
        if escape(form.busorigin.data) not in buses:
            return "There was a problem with your registration information.\nPlease check your information and try again."

        # handle the resume
        resumepath = ''
        f = None
        if 'resumefileinput' in request.files:
            f = request.files['resumefileinput']
            if f and f.filename != '' and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                resumepath = os.path.join(app.config['UPLOAD_FOLDER'], str(int(time.time())) + filename)
            else:
                return "There was a problem with your Resume upload. Make sure it is a doc, docx, pdf, txt, or rtf."
        else:
            return "There was a problem with your Resume upload. Please check your upload and try again."

        # Insert the form data into the db
        hacker = Hacker(form.fname.data, form.lname.data, form.email.data.lower(), form.age.data, form.grade.data, form.school.data, form.busorigin.data, form.webdev.data, form.mobiledev.data, form.arvrdev.data, form.hardwaredev.data, form.aidev.data, form.website.data, form.linkedin.data, form.poem.data, form.techsimplify.data, form.hacktechsuggest.data, form.othercomment.data, form.accept_tos.data, datetime.datetime.utcnow(), resumepath, form.major.data)

        # try to catch people applying with the same email multiple times
        try:
            db.session.add(hacker)
            db.session.commit()
            f.save(resumepath)
        except exc.IntegrityError:
            app.logger.info("Application try from prev app email " + str(escape(form.email.data)))
            return "Stop clicking the Apply button, you've already applied with that email!"

        app.logger.info("Application submitted by " + str(escape(form.email.data)))

        # Now we'll send the email application confirmation
        subject = "Thanks for Applying to Hacktech 2017!"
        html = render_template('JoinTechTemplates/Hacktech2017_submitapplication.html')
        send_email(hacker.email, subject, html, app_log=app.logger)

        return "Thank you for registering, "+escape(form.fname.data)+". We've sent a confirmation link to "+escape(form.email.data)+"."
    elif request.method == 'POST':
        return "There was a problem with your registration information.\nPlease check your information and try again."
    return render_template('JoinTechTemplates/register.html', form=form)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.errorhandler(404)
def page_not_found(e):
    return render_template('JoinTechTemplates/error.html', error_code=404)

@app.errorhandler(403)
def page_not_found(e):
    return render_template('JoinTechTemplates/error.html', error_code=403)

@app.errorhandler(410)
def page_not_found(e):
    return render_template('JoinTechTemplates/error.html', error_code=410)

if __name__ == '__main__':
    app.run()
