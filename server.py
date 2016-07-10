from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, json
import directory

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    return 'Index Page'

@app.route('/leaderboard')
def leaderboard(name=None):
    name = request.args["name"]
    return render_template('leaderboard.html', name=name)
'''
@app.route('/games')
def game(name=None):
    if name is None:
        name = "gamesgamesgames"
    return render_template('games.html')
'''

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

@app.route('/api/trivia_game', methods=['GET', 'POST'])
def trivia():
    if request.method == 'GET':
        key = int(request.args.get('question'))
        if key in directory.TRIVIA_QUESTIONS_LIST:
            return "%d. %s" % (key, directory.TRIVIA_QUESTIONS_LIST[key])
        else:
            return "No questions left! Check back later for more!"
    elif request.method == 'POST':
        answer = request.form["answer"]
        questionNum = int(request.form["question"])

        if (directory.TRIVIA_ANSWERS_LIST[questionNum] == answer):
            return json.dumps({"result": "Correct!"})
        return json.dumps({"result": "Wrong!"})
    return "pls"

@app.route('/play/<gamename>')
def play_game(gamename, username=None):
    username = request.args.get('username')
    if gamename is None or username is None:
        return redirect(url_for('login'))
    return render_template('games/%s.html' % gamename, username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('leaderboard', name=request.form['username']))
    return render_template('login.html', error=error)

if __name__ == "__main__":
    app.run()
