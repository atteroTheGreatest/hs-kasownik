from flask import (Flask, render_template,
                   session, request, flash, redirect,
                   url_for)

import requests
from kasownik_client import APIClient
from flask.ext.cache import Cache


SECRET_KEY = 'development key'
CACHE_TYPE = 'simple'
app = Flask(__name__)
app.config.from_object(__name__)
cache = Cache(app)


@cache.cached(timeout=50)
@app.route('/')
def greet():
    return render_template('index.html', header=get_header())


@cache.cached(timeout=500)
def get_header():
    r = requests.get('http://static.hackerspace.pl/html/topmenu.html')
    return r.text


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
            error = True
    header = get_header()
    return render_template('login.html', error=error, header=header)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('greet'))


@app.route('/payments')
def show_payments():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        kasownik = APIClient()
        username = session['username']
        mana = get_mana()
        user_payments_data = kasownik.get_member_info(member=username)
        print username
        header = get_header()
        return render_template('payments.html', mana=mana,
                                payments=user_payments_data,
                                header=header,
                                username=username,)


@app.template_filter('shorten')
def shorten_filter(s):
    if len(s) > 10:
        return s[:4] + "..." + s[-4:]
    else:
        return s

def get_mana():
    host = 'http://kasownik.hackerspace.pl/api'
    method = "mana.json"
    r = requests.get(host + "/" + method)

    json_response = r.json()
    if r.status_code == 200:
        return json_response['content']
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True, port=3000)
