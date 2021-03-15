from flask import Flask, render_template, request, redirect, url_for, \
    session, flash
from datetime import timedelta
from config import Config
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
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


@app.route('/view')
def view():
    return render_template('view.html', values=users.query.all())


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        name = request.form['name']
        session['name'] = name
        flash('Login Successful!')
        return redirect(url_for('profile'))
    else:
        if 'name' in session:
            flash('Already Logged In!')
            return redirect(url_for('profile'))
        return render_template('login.html')


@app.route('/logout')
def logout():
    flash('You have been logout!', 'info')
    session.pop('name', None)
    session.pop('email', None)
    session.pop('city', None)
    return redirect(url_for('login'))


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        session.permanent = True
        name = request.form['name']
        session['name'] = name
        found_user = users.query.filter_by(name=name).first()
        if found_user:
            flash(f'User {name} already exists. Try another name.')
        else:
            nm = users(name, '', '')
            db.session.add(nm)
            db.session.commit()
            flash('Registration Successful!')
            session.pop('name', None)
            return redirect(url_for('login'))
    return render_template('registration.html')


@app.route('/profile', methods=['POST', 'GET'])
def profile():
    email = None
    city = None
    if 'name' in session:
        name = session['name']
        if request.method == 'POST':
            email = request.form['email']
            session['email'] = email
            city = request.form['city']
            session['city'] = city
            found_user = users.query.filter_by(name=name).first()
            found_user.email = email
            db.session.commit()
            found_user = users.query.filter_by(name=name).first()
            found_user.city = city
            db.session.commit()
            if found_user.city and found_user.email:
                flash('Email and city were changed!')
            elif found_user.city and not found_user.email:
                flash('Only city was changed!')
            elif found_user.email and not found_user.city:
                flash('Only email was changed!')
            else:
                flash('Nothing was changed!')
        else:
            if 'city' in session and 'email' in session:
                city = session['city']
                email = session['email']
            elif 'city' in session:
                city = session['city']
            elif 'email' in session:
                email = session['email']
        return render_template('profile.html', city=city, email=email)
    else:
        flash('You are not logged in!')
        return redirect(url_for('login'))


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        user_name = request.form['user_name']
        found_user = users.query.filter_by(name=user_name).first()
        if found_user:
            users.query.filter_by(name=user_name).delete()
            db.session.commit()
            flash(f'{user_name} have been delete')
        else:
            flash(f'{user_name} not exists')
    return render_template('delete.html')


if __name__ == '__main__':
    db.create_all()
    app.run()