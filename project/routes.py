from flask import Blueprint, render_template, request, jsonify, current_app

from project.utils import request_is_authorized

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

@wiki.route('/webhook', methods=['POST'])
def webhook_event():
    """
    Handles Github POST webhooks, authenticated with secret keys
    """
    if request_is_authorized(request):
        request_params = request.get_json()
        return jsonify('Yep, got it'), 200
    else:
        return jsonify('Invalid security token'), 401