
import pytest
import requests
from tests.support.api_constants import API_USERS_ENDPOINTS, API_MESSAGES
from tests.data.faker_manager import generate_user_data, generate_password
from tests.support.test_utils import read_fixture_data, delete_fixture_data, users_url, create_fixture_key
from tests.support.api_helpers import create_user, login_user, delete_user

@pytest.mark.api
@pytest.mark.api_users
@pytest.mark.full
class TestUsersAPI:

    @pytest.mark.basic
    def test_create_new_user(self):
        """
        This test covers the full user lifecycle: creation, login, and deletion.
        All user flow steps are handled by helpers.
        """
        key = create_fixture_key()
        create_user(key)
        login_user(key)
        delete_user(key)
        delete_fixture_data(key)

    @pytest.mark.negative
    def test_create_new_user_bad_request(self):
        """
        This test covers user registration with invalid email (negative scenario).
        No helpers are used since the user is not created successfully.
        """
        user = generate_user_data()
        response = requests.post(users_url(API_USERS_ENDPOINTS['REGISTER']), json={
            'name': user['user_name'],
            'email': '@' + user['user_email'],
            'password': user['user_password'],
        })
        body = response.json()
        assert response.status_code == 400
        assert body['success'] is False
        assert body['message'] == API_MESSAGES['VALID_EMAIL_REQUIRED']

    @pytest.mark.negative
    @pytest.mark.parametrize("email_mod,password_mod,expected_status,expected_message", [
        (lambda u: '@' + u['user_email'], lambda u: u['user_password'], 400, API_MESSAGES['VALID_EMAIL_REQUIRED']),
        (lambda u: u['user_email'], lambda u: '@' + u['user_password'], 401, API_MESSAGES['INCORRECT_EMAIL_OR_PASSWORD']),
    ])
    def test_login_existing_user_negative(self, email_mod, password_mod, expected_status, expected_message):
        """
        This test covers negative login scenarios using invalid email or password.
        User creation and deletion are handled by helpers.
        """
        key = create_fixture_key()
        create_user(key)
        user = read_fixture_data(key)
        login_resp = requests.post(users_url(API_USERS_ENDPOINTS['LOGIN']), json={
            'email': email_mod(user),
            'password': password_mod(user),
        })
        login_body = login_resp.json()
        assert login_resp.status_code == expected_status
        assert login_body['success'] is False
        assert login_body['message'] == expected_message
        login_user(key)
        delete_user(key)
        delete_fixture_data(key)

    @pytest.mark.basic
    def test_profile_retrieve(self):
        """
        This test covers successful profile retrieval for a valid user.
        User creation, login, and deletion are handled by helpers.
        """
        key = create_fixture_key()
        create_user(key)
        login_user(key)
        user = read_fixture_data(key)
        profile_resp = requests.get(users_url(API_USERS_ENDPOINTS['PROFILE']), headers={'X-Auth-Token': user['user_token']})
        profile_body = profile_resp.json()
        assert profile_resp.status_code == 200
        assert profile_body['success'] is True
        assert profile_body['message'] == API_MESSAGES['PROFILE_SUCCESSFUL']
        assert profile_body['data']['email'] == user['user_email']
        assert profile_body['data']['id'] == user['user_id']
        assert profile_body['data']['name'] == user['user_name']
        delete_user(key)
        delete_fixture_data(key)

    @pytest.mark.negative
    @pytest.mark.parametrize("header_mod,expected_status,expected_message", [
        (lambda t: {'X-Auth-Token': t, 'x-content-format': 'badRequest'}, 400, API_MESSAGES['INVALID_CONTENT_FORMAT']),
        (lambda t: {'X-Auth-Token': '@' + t}, 401, API_MESSAGES['ACCESS_TOKEN_INVALID']),
    ])
    def test_profile_retrieve_negative(self, header_mod, expected_status, expected_message):
        """
        This test covers negative profile retrieval scenarios with invalid headers or tokens.
        User creation, login, and deletion are handled by helpers.
        """
        key = create_fixture_key()
        create_user(key)
        login_user(key)
        user = read_fixture_data(key)
        resp = requests.get(users_url(API_USERS_ENDPOINTS['PROFILE']), headers=header_mod(user['user_token']))
        body = resp.json()
        assert resp.status_code == expected_status
        assert body['success'] is False
        assert body['message'] == expected_message
        delete_user(key)
        delete_fixture_data(key)

    @pytest.mark.basic
    def test_profile_update(self):
        """
        This test covers successful profile update for a valid user.
        User creation, login, and deletion are handled by helpers.
        """
        key = create_fixture_key()
        create_user(key)
        login_user(key)
        user = read_fixture_data(key)
        updated = {
            'name': 'Novo Nome',
            'phone': '11999999999',
            'company': 'Nova Empresa',
        }
        update_resp = requests.patch(users_url(API_USERS_ENDPOINTS['PROFILE']), headers={'X-Auth-Token': user['user_token']}, json=updated)
        update_body = update_resp.json()
        assert update_resp.status_code == 200
        assert update_body['success'] is True
        assert update_body['message'] == API_MESSAGES['PROFILE_UPDATED_SUCCESSFUL']
        assert update_body['data']['name'] == updated['name']
        assert update_body['data']['phone'] == updated['phone']
        assert update_body['data']['company'] == updated['company']
        delete_user(key)
        delete_fixture_data(key)

    @pytest.mark.negative
    @pytest.mark.parametrize("updated,header_mod,expected_status,expected_message", [
        ({'name': '6@#', 'phone': '11999999999', 'company': 'Nova Empresa'}, lambda t: {'X-Auth-Token': t}, 400, API_MESSAGES['USER_NAME_BETWEEN_4_30']),
        ({'name': 'Novo Nome', 'phone': '11999999999', 'company': 'Nova Empresa'}, lambda t: {'X-Auth-Token': '@' + t}, 401, API_MESSAGES['ACCESS_TOKEN_INVALID']),
    ])
    def test_profile_update_negative(self, updated, header_mod, expected_status, expected_message):
        """
        This test covers negative profile update scenarios with invalid data or tokens.
        User creation, login, and deletion are handled by helpers.
        """
        key = create_fixture_key()
        create_user(key)
        login_user(key)
        user = read_fixture_data(key)
        resp = requests.patch(users_url(API_USERS_ENDPOINTS['PROFILE']), headers=header_mod(user['user_token']), json=updated)
        body = resp.json()
        assert resp.status_code == expected_status
        assert body['success'] is False
        assert body['message'] == expected_message
        delete_user(key)
        delete_fixture_data(key)

    @pytest.mark.basic
    def test_change_password(self):
        """
        This test covers the password change flow for a valid user.
        User creation, login, and deletion are handled by helpers.
        """
        key = create_fixture_key()
        create_user(key)
        login_user(key)
        user = read_fixture_data(key)
        new_password = generate_password()
        resp = requests.post(users_url(API_USERS_ENDPOINTS['CHANGE_PASSWORD']), headers={'X-Auth-Token': user['user_token']}, json={
            'currentPassword': user['user_password'],
            'newPassword': new_password,
        })
        body = resp.json()
        assert resp.status_code == 200
        assert body['success'] is True
        assert body['message'] == API_MESSAGES['THE_PASSWORD_WAS_SUCCESSFULLY_UPDATED']
        assert user['user_password'] != new_password
        delete_user(key)
        delete_fixture_data(key)

    @pytest.mark.negative
    @pytest.mark.parametrize("new_password,header_mod,expected_status,expected_message", [
        ('123', lambda t: {'X-Auth-Token': t}, 400, API_MESSAGES['NEW_PASSWORD_BETWEEN_6_30']),
        (None, lambda t: {'X-Auth-Token': '@' + t}, 401, API_MESSAGES['ACCESS_TOKEN_INVALID']),
    ])
    def test_change_password_negative(self, new_password, header_mod, expected_status, expected_message):
        """
        This test covers negative password change scenarios with invalid new password or token.
        User creation, login, and deletion are handled by helpers.
        """
        key = create_fixture_key()
        create_user(key)
        login_user(key)
        user = read_fixture_data(key)
        # If new_password is None, generate a valid one for the unauthorized scenario
        new_password_val = generate_password() if new_password is None else new_password
        resp = requests.post(
            users_url(API_USERS_ENDPOINTS['CHANGE_PASSWORD']),
            headers=header_mod(user['user_token']),
            json={
                'currentPassword': user['user_password'],
                'newPassword': new_password_val,
            }
        )
        body = resp.json()
        assert resp.status_code == expected_status
        assert body['success'] is False
        assert body['message'] == expected_message
        delete_user(key)
        delete_fixture_data(key)

    @pytest.mark.basic
    def test_logout_user(self):
        """
        This test covers successful logout for a valid user.
        User creation, login, and deletion are handled by helpers.
        Note: After logout, login is called again to obtain a valid token for cleanup.
        """
        key = create_fixture_key()
        create_user(key)
        login_user(key)
        user = read_fixture_data(key)
        resp = requests.delete(users_url(API_USERS_ENDPOINTS['LOGOUT']), headers={'X-Auth-Token': user['user_token']})
        body = resp.json()
        assert resp.status_code == 200
        assert body['success'] is True
        assert body['message'] == API_MESSAGES['USER_HAS_BEEN_SUCCESSFULLY_LOGGED_OUT']
        # Clean up: login again to get a valid token for deletion
        login_user(key)
        delete_user(key)
        delete_fixture_data(key)

    @pytest.mark.negative
    @pytest.mark.parametrize("header_mod,expected_status,expected_message", [
        (lambda t: {'X-Auth-Token': t, 'x-content-format': 'badRequest'}, 400, API_MESSAGES['INVALID_CONTENT_FORMAT']),
        (lambda t: {'X-Auth-Token': '@' + t}, 401, API_MESSAGES['ACCESS_TOKEN_INVALID']),
    ])
    def test_logout_user_negative(self, header_mod, expected_status, expected_message):
        """
        This test covers negative logout scenarios with invalid headers or tokens.
        User creation, login, and deletion are handled by helpers.
        """
        key = create_fixture_key()
        create_user(key)
        login_user(key)
        user = read_fixture_data(key)
        resp = requests.delete(users_url(API_USERS_ENDPOINTS['LOGOUT']), headers=header_mod(user['user_token']))
        body = resp.json()
        assert resp.status_code == expected_status
        assert body['success'] is False
        assert body['message'] == expected_message
        delete_user(key)
        delete_fixture_data(key)

    @pytest.mark.negative
    @pytest.mark.parametrize("header_mod,expected_status,expected_message", [
        (lambda t: {'X-Auth-Token': t, 'x-content-format': 'badRequest'}, 400, API_MESSAGES['INVALID_CONTENT_FORMAT']),
        (lambda t: {'X-Auth-Token': '@' + t}, 401, API_MESSAGES['ACCESS_TOKEN_INVALID']),
    ])
    def test_delete_account_negative(self, header_mod, expected_status, expected_message):
        """
        This test covers negative account deletion scenarios with invalid headers or tokens.
        User creation, login, and deletion are handled by helpers.
        """
        key = create_fixture_key()
        create_user(key)
        login_user(key)
        user = read_fixture_data(key)
        resp = requests.delete(users_url(API_USERS_ENDPOINTS['DELETE_ACCOUNT']), headers=header_mod(user['user_token']))
        body = resp.json()
        assert resp.status_code == expected_status
        assert body['success'] is False
        assert body['message'] == expected_message
        delete_user(key)
        delete_fixture_data(key)
        

