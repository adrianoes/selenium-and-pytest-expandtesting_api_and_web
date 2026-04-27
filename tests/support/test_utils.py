from tests.support.api_constants import API_USERS_BASE, API_NOTES_BASE
import os
import json

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), '../fixtures/tmp_data')

# Utility to create a unique fixture key
def create_fixture_key():
    import uuid
    return str(uuid.uuid4())

# Helper to delete an authenticated user (for legacy/test cleanup only)
def delete_user_with_login(fixture_key, token=None):
    from tests.support.test_utils import read_fixture_data, users_url
    import requests
    try:
        user = read_fixture_data(fixture_key)
        if not token:
            # Try to login to get token
            login_resp = requests.post(users_url('login'), json={
                'email': user['user_email'],
                'password': user['user_password'],
            })
            login_body = login_resp.json()
            token = login_body['data']['token']
        requests.delete(users_url('delete-account'), headers={'X-Auth-Token': token})
    except Exception:
        pass

def fixture_path(key):
    return os.path.join(FIXTURE_DIR, f'testdata-{key}.json')

def save_fixture_data(key, data):
    os.makedirs(FIXTURE_DIR, exist_ok=True)
    with open(fixture_path(key), 'w', encoding='utf-8') as f:
        json.dump(data, f)

def read_fixture_data(key):
    with open(fixture_path(key), 'r', encoding='utf-8') as f:
        return json.load(f)

def delete_fixture_data(key):
    try:
        os.remove(fixture_path(key))
    except FileNotFoundError:
        pass

def users_url(path):
    return f"{API_USERS_BASE}{path}"

def notes_url(path=''):
    return f"{API_NOTES_BASE}{path}"
