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
    return render_template('leaderboard.html', name=name, game_name=directory.GAME_NAME_LIST, game_desc=directory.GAME_DESCRIPTION_LIST, game_link=directory.GAME_LINK_LIST)
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
    if request.method == 'POST':
        answer = request.form["answer"]
        questionNum = request.form["question"]
        if (dictionary.TRIVIA_ANSWERS_LIST[questioNum] == answer):
            return "Correct!"
        return "Wrong!"

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
        if request.form['username'] in directory.USER_TO_PASS_LIST.keys():
            if request.form['password'] == directory.USER_TO_PASS_LIST[request.form['username']]:
                return redirect(url_for('leaderboard', name=request.form['username']))
            error = 'Invalid Credentials. Please try again.'
        error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

if __name__ == "__main__":
    app.run()
