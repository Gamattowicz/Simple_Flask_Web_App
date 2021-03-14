from flask import Flask, render_template, request, redirect, url_for, \
    session, flash
from datetime import timedelta
from config import Config
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)


class users(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    city = db.Column(db.String(50))

    def __init__(self, name, email, city):
        self.name = name
        self.email = email
        self.city = city


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        name = request.form['nm']
        session['name'] = name
        flash('Login Successful!')
        return redirect(url_for('welcome'))
    else:
        if 'name' in session:
            flash('Already Logged In!')
            return redirect(url_for('welcome'))

        return render_template('login.html')


@app.route('/welcome', methods=['POST', 'GET'])
def welcome():
    email = None
    if 'name' in session:
        name = session['name']

        if request.method == 'POST':
            email = request.form['email']
            session['email'] = email
            flash('Email was saved!')
        else:
            if 'email' in session:
                email = session['email']

        return render_template('welcome.html', email=email)
    else:
        flash('You are not logged in!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    flash('You have been logout!', 'info')
    session.pop('name', None)
    session.pop('email', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    db.create_all()
    app.run()