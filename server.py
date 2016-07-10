from flask import Flask, flash, redirect, render_template, request, session, abort, url_for

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    return 'Index Page'

@app.route('/leaderboard')
def leaderboard(name=None):
    name = request.args["name"]
    return render_template('leaderboard.html', name=name)

@app.route('/games')
def game():
    if name is None:
        name = "gamesgamesgames"
    return render_template('games.html')

@app.route('/api/code_golf')
def golf(username=None):
    user_code = request.args.get('code')
    question = "Check if a given positive integer is divisible by 2."
    #test_cases = {0 : True, 5 : False, 4: True, 1024 : True
    test_case = 5
    try:

        print eval(user_code[1:-1])
        if eval(user_code) == test_case:
            return "success"
        return "failure - wrong answer"
    except:
        return "failure - invalid eval"

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
