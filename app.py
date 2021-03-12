from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/<name>')
def welcome(name):
    return render_template('welcome.html', name=f'Hey {name}')


if __name__ == '__main__':
    app.run(debug=True)