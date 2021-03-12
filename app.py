from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return 'Home page'


@app.route('/<name>')
def welcome(name):
    return f'Hey {name}'


if __name__ == '__main__':
    app.run(debug=True)