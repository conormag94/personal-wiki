import hashlib
import hmac

from flask import current_app

def get_changed_files(payload_json):
    updated = []
    deleted = []
    
    for commit in payload_json['commits']:
        for file in commit['added']:
            updated.append(file)
        for file in commit['modified']:
            updated.append(file)
        
        for file in commit['removed']:
            deleted.append(file)
            if file in updated:
                updated.remove(file)

    return (updated, deleted)


def verify_signature(received_signature, payload_body):
    """
    Hashes the request payload using the secret and compares it with the
    hash signature received by the Github webhook.
    """
    key = current_app.config['SECRET_KEY'].encode()
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
    if current_app.config['VERIFY_WEBHOOKS'] is False:
        return True

    received_signature = request.headers.get('X-Hub-Signature')
    if received_signature and verify_signature(received_signature, request.data):
        return True

    return False