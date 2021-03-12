from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
app.permanent_session_lifetime = timedelta(minutes=5)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        name = request.form['nm']
        session['name'] = name
        return redirect(url_for('welcome'))
    else:
        if 'name' in session:
            return redirect(url_for('welcome'))
        return render_template('login.html')


@app.route('/welcome')
def welcome():
    if 'name' in session:
        name = session['name']
        return render_template('welcome.html', name=name)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('name', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)