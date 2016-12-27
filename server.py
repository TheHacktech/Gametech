from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, json
import directory
import re
import random

app = Flask(__name__)
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
    if request.method == 'GET':
        key = int(request.args.get('question'))
        if key in directory.TRIVIA_QUESTIONS_LIST:
            return "%d. %s" % (key, directory.TRIVIA_QUESTIONS_LIST[key])
        else:
            return "No questions left! Check back later for more!"
    elif request.method == 'POST':
        answer = normalize(request.form["answer"])
        questionNum = int(request.form["question"])

        if (directory.TRIVIA_ANSWERS_LIST[questionNum] == answer):
            return json.dumps({"result": "Correct!"})
        return json.dumps({"result": "Wrong!"})
    return "pls"

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
    app.run(port=1234)
