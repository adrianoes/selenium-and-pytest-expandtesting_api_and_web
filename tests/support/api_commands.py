from tests.support.api_constants import API_USERS_BASE, API_NOTES_BASE
import os
import json

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), '../fixtures/tmp_data')

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
