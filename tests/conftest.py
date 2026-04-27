import pytest
import os
import json
from tests.data.faker_manager import generate_user_data, generate_note_data, generate_note_update_data, generate_password

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'data')

@pytest.fixture
def user_data():
    return generate_user_data()

@pytest.fixture
def note_data():
    return generate_note_data()

@pytest.fixture
def note_update_data():
    return generate_note_update_data()

@pytest.fixture
def password():
    return generate_password()

@pytest.fixture
def fixture_key():
    import uuid
    return str(uuid.uuid4())

@pytest.fixture
def save_fixture():
    def _save(key, data):
        os.makedirs(FIXTURE_DIR, exist_ok=True)
        with open(os.path.join(FIXTURE_DIR, f'testdata-{key}.json'), 'w', encoding='utf-8') as f:
            json.dump(data, f)
    return _save

@pytest.fixture
def read_fixture():
    def _read(key):
        with open(os.path.join(FIXTURE_DIR, f'testdata-{key}.json'), 'r', encoding='utf-8') as f:
            return json.load(f)
    return _read

@pytest.fixture
def delete_fixture():
    def _delete(key):
        try:
            os.remove(os.path.join(FIXTURE_DIR, f'testdata-{key}.json'))
        except FileNotFoundError:
            pass
    return _delete
