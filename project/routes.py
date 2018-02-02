from flask import Blueprint, render_template, request, jsonify, current_app

from project import db
from project.models import Note
from project.utils import request_is_authorized, get_changed_files, get_file_contents, remove_note_template

wiki = Blueprint('wiki', __name__)


@wiki.route('/', methods=['GET'])
def index():
    notes = Note.query.all()
    return render_template('index.html', title='Home', notes=notes)


@wiki.route('/<int:note_id>', methods=['GET'])
def view_note(note_id):
    note = Note.query.filter_by(id=note_id).first_or_404()
    print(note.template_file)
    return render_template('view_note.html', note=note)


@wiki.route('/webhook', methods=['POST'])
def webhook_event():
    """
    Handles Github POST webhooks, authenticated with secret keys
    """
    if request_is_authorized(request):
        request_params = request.get_json()
        added, updated, removed = get_changed_files(payload_json=request_params)

        response_message = {
            'status': 'Success',
            'changes': {
                'added': added,
                'updated': updated,
                'removed': removed
            }
        }

        for file in added:
            markdown = get_file_contents(file)
            note = Note(filename=file, markdown=markdown)
            db.session.add(note)
            db.session.commit()

        for file in updated:
            new_markdown = get_file_contents(file)
            note = Note.query.filter_by(filename=file).first()
            note.update(new_markdown)
            db.session.commit()

        for file in removed:
            note = Note.query.filter_by(filename=file).first()
            if note:
                db.session.delete(note)
                db.session.commit()
                remove_note_template(note.id)

        return jsonify(response_message), 200
    else:
        return jsonify('Invalid security token'), 401