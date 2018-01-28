from flask import Blueprint, render_template, request, jsonify, current_app

from project.models import Note
from project.utils import request_is_authorized, get_changed_files, get_file_contents

wiki = Blueprint('wiki', __name__)

@wiki.route('/', methods=['GET'])
def index():
    notes = Note.query.all()
    return render_template('index.html', title='Home', notes=notes)

@wiki.route('/<note_id>', methods=['GET'])
def read_note(note_id):
    note = Note.query.filter_by(id=note_id).first_or_404()
    return render_template('note.html', note=note)

@wiki.route('/webhook', methods=['POST'])
def webhook_event():
    """
    Handles Github POST webhooks, authenticated with secret keys
    """
    if request_is_authorized(request):
        request_params = request.get_json()
        updated, removed = get_changed_files(payload_json=request_params)

        response_message = {
            'status': 'Success',
            'changes': {
                'updated': updated,
                'removed': removed
            }
        }
        for file in updated:
            print(get_file_contents(file))
        return jsonify(response_message), 200
    else:
        return jsonify('Invalid security token'), 401