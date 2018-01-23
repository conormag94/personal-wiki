from flask import Blueprint, render_template, current_app

wiki = Blueprint('wiki', __name__)

@wiki.route('/', methods=['GET'])
def index():
    notes = [
        {
            'title': 'Note 1',
            'content': 'The first note'
        },
        {
            'title': 'Note 2',
            'content': 'This is the second note'
        }
    ]
    return render_template('index.html', title='Home', notes=notes)