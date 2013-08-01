from flask import (Flask, render_template, abort,
                   session, request, flash, redirect,
                   url_for)


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
        if True:
            username = request.form['username']
            password = request.form['password']
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_payments'))
            print password, username
        else:
            error = "I don't like you"

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('greet'))


@app.route('/payments')
def show_payments():
    if not session.get('logged_in'):
        abort(401)
    return render_template('payments.html')

if __name__ == '__main__':
    app.run(debug=True)
