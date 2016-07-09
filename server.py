from flask import Flask, flash, redirect, render_template, request, session, abort, url_for


app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    return 'Index Page'

@app.route('/games')
def game():
    if name is None:
        name = "gamesgamesgames"
    return render_template('games.html')

@app.route('/hello')
def hello(name=None):
    if name is None:
        name = "Chenchenchenchenchen"
    return render_template('hello.html', name=name)

@app.route('/play/<gamename>')
def play_game(gamename, username=None):
    username = request.args.get('username')
    if gamename is None or username is None:
        return redirect(url_for('login'))
    return render_template('games/%s.html' % gamename)

@app.route('/log', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('hello'))
    return render_template('login.html', error=error)

if __name__ == "__main__":
    app.run()
