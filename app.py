from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/<name>')
def welcome(name):
    return render_template('welcome.html', name=f'Hey {name}')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('welcome', name=user))
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)