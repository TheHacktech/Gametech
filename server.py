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
