from flask import (Flask, render_template, abort,
                   session, request, flash, redirect,
                   url_for)

import requests
from kasownik_client import APIClient, APIClientException

SECRET_KEY = 'development key'
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def greet():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        login_credentials = {"login": username,
                             "password": password}
        auth_website = 'https://auth.hackerspace.pl'
        r = requests.post(auth_website, login_credentials)
        if r.status_code == 200:
            session['logged_in'] = True
            session['username'] = username
            flash('You were logged in')
            return redirect(url_for('show_payments'))
        else:
            flash('Authorization error,'
                  ' login or password incorrect!')

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('greet'))


@app.route('/payments')
def show_payments():
    if not session.get('logged_in'):
        redirect(url_for('login'))
    kasownik = APIClient()
    mana = kasownik.mana()
    username = session['username']
    user_payments_data = kasownik.member_info(member=username)
    return render_template('payments.html', mana=mana,
                            payments=user_payments_data)

if __name__ == '__main__':
    app.run(debug=True)
