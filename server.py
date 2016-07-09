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

@app.route('/games/<gamename>')
def show_user_profile(gamename):
    # show the user profile for that user
    # return 'Game %s' % gamename
    return render_template(str(gamename) + '.html')

@app.route('/games/submit')
def submit(gamename):
    # show the user profile for that user
    # return 'Game %s' % gamename
    return "you made it"


@app.route('/hello')
def hello(name=None):
    if name is None:
        name = "Chenchenchenchenchen"
    return render_template('hello.html', name=name)

@app.route('/play/parrot_game')
def parrot_game(username=None):
    if username is None:
        redirect(url_for('login'))
    return "SQUAWK"

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
