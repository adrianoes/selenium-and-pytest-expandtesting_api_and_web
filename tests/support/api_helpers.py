# Helper functions for user API flows
import requests
from tests.data.faker_manager import generate_user_data
from tests.support.api_constants import API_USERS_ENDPOINTS
from tests.support.test_utils import users_url, save_fixture_data, read_fixture_data, delete_fixture_data
from tests.support.api_constants import API_MESSAGES
from tests.support.test_utils import notes_url
from tests.data.faker_manager import generate_note_data

def create_user(fixture_key):
    """
    Creates a user via API, saves it in the fixture, and performs detailed assertions.
    """
    user = generate_user_data()
    reg_resp = requests.post(users_url(API_USERS_ENDPOINTS['REGISTER']), json={
        'name': user['user_name'],
        'email': user['user_email'],
        'password': user['user_password'],
    })
    reg_body = reg_resp.json()
    assert reg_resp.status_code == 201, f"Status esperado 201, recebido {reg_resp.status_code}"
    assert reg_body['success'] is True
    assert reg_body['status'] == 201
    from tests.support.api_constants import API_MESSAGES
    assert reg_body['message'] == API_MESSAGES['USER_ACCOUNT_CREATED_SUCCESSFULLY']
    assert 'id' in reg_body['data']
    assert reg_body['data']['email'] == user['user_email']
    assert reg_body['data']['name'] == user['user_name']
    save_fixture_data(fixture_key, {
        'user_email': user['user_email'],
        'user_id': reg_body['data']['id'],
        'user_name': user['user_name'],
        'user_password': user['user_password'],
    })
    return reg_resp, reg_body

def login_user(fixture_key):
    """
    Logs in the user saved in the fixture, performs assertions, and updates the token in the fixture.
    """
    user = read_fixture_data(fixture_key)
    login_resp = requests.post(users_url(API_USERS_ENDPOINTS['LOGIN']), json={
        'email': user['user_email'],
        'password': user['user_password'],
    })
    login_body = login_resp.json()
    assert login_resp.status_code == 200, f"Status esperado 200, recebido {login_resp.status_code}"
    from tests.support.api_constants import API_MESSAGES
    assert login_body['success'] is True
    assert login_body['message'] == API_MESSAGES['LOGIN_SUCCESSFUL']
    assert login_body['data']['email'] == user['user_email']
    assert 'id' in login_body['data']
    assert login_body['data']['name'] == user['user_name']
    user['user_token'] = login_body['data']['token']
    save_fixture_data(fixture_key, user)
    return login_resp, login_body

def delete_user(fixture_key):
    """
    Deletes the authenticated user via API, performs assertions, and removes the fixture.
    Always reads the token from the fixture data.
    """
    user = read_fixture_data(fixture_key)
    token = user.get('user_token')
    if not token:
        raise Exception("No token found in fixture. Please login the user before calling delete_user.")
    del_resp = requests.delete(users_url(API_USERS_ENDPOINTS['DELETE_ACCOUNT']), headers={'X-Auth-Token': token})
    del_body = del_resp.json()
    from tests.support.api_constants import API_MESSAGES
    assert del_resp.status_code == 200, f"Status esperado 200, recebido {del_resp.status_code}"
    assert del_body['message'] == API_MESSAGES['ACCOUNT_DELETED_SUCCESSFULLY']
    delete_fixture_data(fixture_key)

def create_note(fixture_key, note_data=None):
    """
    Cria uma nota via API, salva no fixture, faz asserts e retorna resposta/body.
    """
    user = read_fixture_data(fixture_key)
    note = note_data or generate_note_data()
    resp = requests.post(notes_url(), headers={'X-Auth-Token': user['user_token']}, json={
        'category': note['category'],
        'description': note['description'],
        'title': note['title'],
    })
    body = resp.json()
    assert resp.status_code == 200, f"Status esperado 200, recebido {resp.status_code}"
    assert body['success'] is True
    assert body['message'] == API_MESSAGES['NOTE_SUCCESSFULLY_CREATED']
    assert body['data']['category'] == note['category']
    assert body['data']['description'] == note['description']
    assert body['data']['title'] == note['title']
    assert body['data']['user_id'] == user['user_id']
    save_fixture_data(fixture_key, {
        **user,
        'note_id': body['data']['id'],
        'note_category': body['data']['category'],
        'note_description': body['data']['description'],
        'note_title': body['data']['title'],
        'note_completed': body['data'].get('completed', False),
    })
    return resp, body

def delete_note(fixture_key):
    """
    Deleta a nota criada via API e remove do fixture.
    """
    user = read_fixture_data(fixture_key)
    note_id = user.get('note_id')
    if note_id:
        resp = requests.delete(notes_url(f"/{note_id}"), headers={'X-Auth-Token': user['user_token']})
        body = resp.json()
        assert resp.status_code == 200
        assert body['message'] == API_MESSAGES['NOTE_SUCCESSFULLY_DELETED']
        for k in ['note_id', 'note_category', 'note_description', 'note_title', 'note_completed']:
            user.pop(k, None)
        save_fixture_data(fixture_key, user)
