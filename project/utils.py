import glob
import hashlib
import hmac
import os

from base64 import b64decode

import markdown2
import requests
from flask import current_app as app

basedir = os.path.abspath(os.path.dirname(__file__))


def remove_note_template(note_id):
    """Remove a note's html template file after it has been deleted."""
    filename = f'{basedir}/templates/notes/{note_id}.html'
    try:
        os.remove(filename)
        print(f'File {filename} deleted')
    except OSError:
        print(f'File {filename} does not exist')


def remove_all_note_templates():
    """
    Remove all html note templates from the directory, except for the
    placeholder template, 0.html
    """
    directory = f'{basedir}/templates/notes/*.html'
    files = glob.glob(directory)

    for file in files:
        if '/0.html' not in file:
            os.remove(file)


def markdown_to_html(markdown_string):
    html = markdown2.markdown(markdown_string, extras=['fenced-code-blocks'])
    return html


def files_in_repo():
    """
    Query the Github API for a list of all the markdown files in the repo.
    """
    USERNAME = app.config['GITHUB_USERNAME']
    TOKEN = app.config['GITHUB_API_KEY']

    BASE_URL = f'https://api.github.com/repos/{USERNAME}/notes'

    markdown_files = []

    url = f'{BASE_URL}/git/trees/HEAD?recursive=1'
    r = requests.get(url, auth=(USERNAME, TOKEN)).json()

    for file in r['tree']:
        if file['path'].endswith('.md'):
            markdown_files.append(file['path'])

    return markdown_files


def get_file_contents(filename):
    """
    Return the contents of <filename>, as bytes (decoded from base64).
    """
    USERNAME = app.config['GITHUB_USERNAME']
    TOKEN = app.config['GITHUB_API_KEY']

    BASE_URL = f'https://api.github.com/repos/{USERNAME}/notes'

    url = f'{BASE_URL}/contents/{filename}'
    r = requests.get(url, auth=(USERNAME, TOKEN))

    encoded_content = r.json()['content']
    decoded_content = b64decode(encoded_content)

    return decoded_content


def get_changed_files(payload_json):
    """
    Get files which have been updated or deleted since the last push.

    Returns a tuple of lists: (added, updated, deleted).
    """
    added = []
    updated = []
    deleted = []

    for commit in payload_json['commits']:
        for file in commit['added']:
            added.append(file)
        for file in commit['modified']:
            updated.append(file)

        for file in commit['removed']:
            deleted.append(file)
            if file in added:
                added.remove(file)
            if file in updated:
                updated.remove(file)

    return added, updated, deleted


def verify_signature(received_signature, payload_body):
    """
    Hashes the request payload using the secret and compares it with the
    hash signature received by the Github webhook.
    """
    key = app.config['SECRET_KEY'].encode()
    hasher = hmac.new(key, payload_body, hashlib.sha1)

    hashed_signature = 'sha1=' + hasher.hexdigest()
    return hmac.compare_digest(hashed_signature, received_signature)


def request_is_authorized(request):
    """
    A webhook POST request is authorized under two conditions:

    1. `VERIFY_WEBHOOKS` in config.py is False (debugging purposes).
    2. `VERIFY_WEBHOOKS` is True and the signature header is verified, using
       the `verify_signature()` function. 
    """
    if app.config['VERIFY_WEBHOOKS'] is False:
        return True

    received_signature = request.headers.get('X-Hub-Signature')
    if received_signature and verify_signature(received_signature, request.data):
        return True

    return False
