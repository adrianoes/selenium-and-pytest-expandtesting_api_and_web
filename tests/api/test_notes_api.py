import pytest
import requests
from tests.support.api_constants import API_MESSAGES
from tests.data.faker_manager import generate_note_data, generate_note_update_data
from tests.support.test_utils import notes_url, create_fixture_key, read_fixture_data, delete_fixture_data
from tests.support.api_helpers import create_user, login_user, delete_user, create_note, delete_note

@pytest.mark.api
@pytest.mark.api_notes
@pytest.mark.full
class TestNotesAPI:
    @pytest.mark.basic
    def test_create_note(self):
        """
        This test covers the creation of a valid note.
        User and note are created by helpers, cleanup is guaranteed.
        """
        key = create_fixture_key()
        create_user(key)
        login_user(key)
        create_note(key)
        delete_note(key)
        delete_user(key)
        delete_fixture_data(key)

    @pytest.mark.negative
    @pytest.mark.parametrize("category,header_mod,expected_status,expected_message", [
        ('invalid', lambda t: {'X-Auth-Token': t}, 400, API_MESSAGES['CATEGORY_INVALID']),
        ('Home', lambda t: {'X-Auth-Token': '@' + t}, 401, API_MESSAGES['ACCESS_TOKEN_INVALID']),
    ])
    def test_create_note_negative(self, category, header_mod, expected_status, expected_message):
        """
        This test covers negative scenarios for note creation (invalid category, invalid token).
        """
        key = create_fixture_key()
        create_user(key)
        login_user(key)
        user = read_fixture_data(key)
        note = generate_note_data()
        note['category'] = category
        resp = requests.post(notes_url(), headers=header_mod(user['user_token']), json={
            'category': note['category'],
            'description': note['description'],
            'title': note['title'],
        })
        body = resp.json()
        assert resp.status_code == expected_status
        assert body['success'] is False
        assert body['message'] == expected_message
        delete_user(key)
        delete_fixture_data(key)

    @pytest.mark.basic
    def test_get_all_notes(self):
        """
        This test covers retrieving all notes for a user.
        Creates multiple notes, asserts retrieval, and cleans up.
        """
        key = create_fixture_key()
        create_user(key)
        login_user(key)
        user = read_fixture_data(key)
        notes = [generate_note_data() for _ in range(4)]
        categories = [notes[0]['category'], 'Home', 'Work', 'Personal']
        completed = [False, False, False, True]
        titles = [n['title'] for n in notes]
        descriptions = [n['description'] for n in notes]
        note_ids = []
        for i in range(4):
            resp, body = create_note(key, {
                'category': categories[i],
                'completed': completed[i],
                'description': descriptions[i],
                'title': titles[i],
            })
            assert body['message'] == API_MESSAGES['NOTE_SUCCESSFULLY_CREATED']
            note_ids.append(body['data']['id'])
        resp = requests.get(notes_url(), headers={'X-Auth-Token': user['user_token']})
        body = resp.json()
        assert resp.status_code == 200
        assert body['success'] is True
        assert body['message'] == API_MESSAGES['NOTES_SUCCESSFULLY_RETRIEVED']
        assert isinstance(body['data'], list)
        assert len(body['data']) >= 4
        # Clean up
        delete_note(key)
        delete_user(key)
        delete_fixture_data(key)

    @pytest.mark.negative
    @pytest.mark.parametrize("header_mod,expected_status,expected_message", [
        (lambda t: {'X-Auth-Token': t, 'x-content-format': 'badRequest'}, 400, API_MESSAGES['INVALID_CONTENT_FORMAT']),
        (lambda t: {'X-Auth-Token': '@' + t}, 401, API_MESSAGES['ACCESS_TOKEN_INVALID']),
    ])
    def test_get_all_notes_negative(self, header_mod, expected_status, expected_message):
        """
        This test covers negative scenarios for retrieving all notes (bad request, unauthorized).
        """
        key = create_fixture_key()
        create_user(key)
        login_user(key)
        user = read_fixture_data(key)
        for _ in range(2):
            create_note(key)
        resp = requests.get(notes_url(), headers=header_mod(user['user_token']))
        body = resp.json()
        assert resp.status_code == expected_status
        assert body['success'] is False
        assert body['message'] == expected_message
        delete_note(key)
        delete_user(key)
        delete_fixture_data(key)

    @pytest.mark.basic
    def test_get_note_by_id(self):
        """
        This test covers retrieving a note by its ID.
        """
        key = create_fixture_key()
        create_user(key)
        login_user(key)
        create_note(key)
        user = read_fixture_data(key)
        note_id = user['note_id']
        resp = requests.get(notes_url(f"/{note_id}"), headers={'X-Auth-Token': user['user_token']})
        body = resp.json()
        assert resp.status_code == 200
        assert body['success'] is True
        assert body['message'] == API_MESSAGES['NOTE_SUCCESSFULLY_RETRIEVED']
        assert body['data']['id'] == note_id
        assert body['data']['title'] == user['note_title']
        assert body['data']['description'] == user['note_description']
        assert body['data']['user_id'] == user['user_id']
        delete_note(key)
        delete_user(key)
        delete_fixture_data(key)

    @pytest.mark.negative
    @pytest.mark.parametrize("header_mod,expected_status,expected_message", [
        (lambda t: {'X-Auth-Token': t, 'x-content-format': 'badRequest'}, 400, API_MESSAGES['INVALID_CONTENT_FORMAT']),
        (lambda t: {'X-Auth-Token': '@' + t}, 401, API_MESSAGES['ACCESS_TOKEN_INVALID']),
    ])
    def test_get_note_by_id_negative(self, header_mod, expected_status, expected_message):
        """
        This test covers negative scenarios for retrieving a note by ID (bad request, unauthorized).
        """
        key = create_fixture_key()
        create_user(key)
        login_user(key)
        create_note(key)
        user = read_fixture_data(key)
        note_id = user['note_id']
        resp = requests.get(notes_url(f"/{note_id}"), headers=header_mod(user['user_token']))
        body = resp.json()
        assert resp.status_code == expected_status
        assert body['success'] is False
        assert body['message'] == expected_message
        delete_note(key)
        delete_user(key)
        delete_fixture_data(key)

    @pytest.mark.basic
    def test_update_note(self):
        """
        This test covers updating an existing note.
        """
        key = create_fixture_key()
        create_user(key)
        login_user(key)
        create_note(key)
        user = read_fixture_data(key)
        note_id = user['note_id']
        note_update = generate_note_update_data()
        updated_note = {
            'category': user['note_category'],
            'completed': note_update['completed'],
            'description': note_update['description'],
            'title': note_update['title'],
        }
        resp = requests.put(notes_url(f"/{note_id}"), headers={'X-Auth-Token': user['user_token']}, json=updated_note)
        body = resp.json()
        assert resp.status_code == 200
        assert body['success'] is True
        assert body['message'] == API_MESSAGES['NOTE_SUCCESSFULLY_UPDATED']
        assert body['data']['description'] == updated_note['description']
        assert body['data']['title'] == updated_note['title']
        assert body['data']['completed'] == updated_note['completed']
        delete_note(key)
        delete_user(key)
        delete_fixture_data(key)

    @pytest.mark.negative
    @pytest.mark.parametrize("category,header_mod,expected_status,expected_message", [
        ('invalid', lambda t: {'X-Auth-Token': t}, 400, API_MESSAGES['CATEGORY_INVALID']),
        ('Home', lambda t: {'X-Auth-Token': '@' + t}, 401, API_MESSAGES['ACCESS_TOKEN_INVALID']),
    ])
    def test_update_note_negative(self, category, header_mod, expected_status, expected_message):
        """
        This test covers negative scenarios for updating a note (invalid category, unauthorized).
        """
        key = create_fixture_key()
        create_user(key)
        login_user(key)
        create_note(key)
        user = read_fixture_data(key)
        note_id = user['note_id']
        note_update = generate_note_update_data()
        update_data = {
            'category': category,
            'completed': False,
            'description': note_update['description'],
            'title': note_update['title'],
        }
        resp = requests.put(notes_url(f"/{note_id}"), headers=header_mod(user['user_token']), json=update_data)
        body = resp.json()
        assert resp.status_code == expected_status
        assert body['success'] is False
        assert body['message'] == expected_message
        delete_note(key)
        delete_user(key)
        delete_fixture_data(key)

    @pytest.mark.basic
    def test_patch_note_completed(self):
        """
        This test covers updating the completed status of a note.
        """
        key = create_fixture_key()
        create_user(key)
        login_user(key)
        create_note(key)
        user = read_fixture_data(key)
        note_id = user['note_id']
        resp = requests.patch(notes_url(f"/{note_id}"), headers={'X-Auth-Token': user['user_token']}, json={'completed': False})
        body = resp.json()
        assert resp.status_code == 200
        assert body['success'] is True
        assert body['message'] == API_MESSAGES['NOTE_SUCCESSFULLY_UPDATED']
        assert body['data']['completed'] is False
        delete_note(key)
        delete_user(key)
        delete_fixture_data(key)

    @pytest.mark.negative
    @pytest.mark.parametrize("completed_val,header_mod,expected_status,expected_message", [
        ('invalid', lambda t: {'X-Auth-Token': t}, 400, API_MESSAGES['NOTE_COMPLETED_MUST_BE_BOOLEAN']),
        (False, lambda t: {'X-Auth-Token': '@' + t}, 401, API_MESSAGES['ACCESS_TOKEN_INVALID']),
    ])
    def test_patch_note_completed_negative(self, completed_val, header_mod, expected_status, expected_message):
        """
        This test covers negative scenarios for patching note completed status (invalid value, unauthorized).
        """
        key = create_fixture_key()
        create_user(key)
        login_user(key)
        create_note(key)
        user = read_fixture_data(key)
        note_id = user['note_id']
        resp = requests.patch(notes_url(f"/{note_id}"), headers=header_mod(user['user_token']), json={'completed': completed_val})
        body = resp.json()
        assert resp.status_code == expected_status
        assert body['success'] is False
        assert body['message'] == expected_message
        delete_note(key)
        delete_user(key)
        delete_fixture_data(key)

    @pytest.mark.basic
    def test_delete_note(self):
        """
        This test covers deleting a note by its ID.
        """
        key = create_fixture_key()
        create_user(key)
        login_user(key)
        create_note(key)
        user = read_fixture_data(key)
        note_id = user['note_id']
        resp = requests.delete(notes_url(f"/{note_id}"), headers={'X-Auth-Token': user['user_token']})
        body = resp.json()
        assert resp.status_code == 200
        assert body['success'] is True
        assert body['message'] == API_MESSAGES['NOTE_SUCCESSFULLY_DELETED']
        delete_user(key)
        delete_fixture_data(key)

    @pytest.mark.negative
    @pytest.mark.parametrize("note_id_mod,header_mod,expected_status,expected_message", [
        (lambda nid: f"+{nid}", lambda t: {'X-Auth-Token': t}, 400, API_MESSAGES['NOTE_ID_MUST_BE_VALID']),
        (lambda nid: nid, lambda t: {'X-Auth-Token': '@' + t}, 401, API_MESSAGES['ACCESS_TOKEN_INVALID']),
    ])
    def test_delete_note_negative(self, note_id_mod, header_mod, expected_status, expected_message):
        """
        This test covers negative scenarios for deleting a note (invalid id, unauthorized).
        """
        key = create_fixture_key()
        create_user(key)
        login_user(key)
        create_note(key)
        user = read_fixture_data(key)
        note_id = user['note_id']
        resp = requests.delete(notes_url(f"/{note_id_mod(note_id)}"), headers=header_mod(user['user_token']))
        body = resp.json()
        assert resp.status_code == expected_status
        assert body['success'] is False
        assert body['message'] == expected_message
        delete_note(key)
        delete_user(key)
        delete_fixture_data(key)




 

