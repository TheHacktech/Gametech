from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    return 'Index Page'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # do_the_login()
        return "LOGIN U BUTT"
    else:
        # show_the_login_form()
        return "GIMME YOUR LOGIN INFO"

@app.route('/games')
def game():
    if name is None:
        name = "gamesgamesgames"
    return render_template('games.html')

@app.route('/games/<gamename>')
def show_user_profile(gamename):
    # show the user profile for that user
    return 'Game %s' % gamename


@app.route('/hello')
def hello(name=None):
    if name is None:
        name = "Chenchenchenchenchen"
    return render_template('hello.html', name=name)


if __name__ == "__main__":
    app.run()



