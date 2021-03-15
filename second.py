from flask import Blueprint

second = Blueprint('second', __name__, template_folder='templates')


@second.route('/test')
def tenant():
    return '<h1>TEST</h1>'