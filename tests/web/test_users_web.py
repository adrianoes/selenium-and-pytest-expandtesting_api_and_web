import pytest
from tests.support.web_helpers import create_user_via_web, login_user_via_web, delete_user_via_web
from tests.support.test_utils import create_fixture_key, delete_fixture_data, read_fixture_data
from conftest import BASE_URL
from tests.web.pages.home_page import HomePage
from tests.web.pages.login_page import LoginPage
from tests.web.pages.profile_page import ProfilePage
from tests.web.pages.register_page import RegisterPage
from tests.data.faker_manager import generate_user_data, generate_password

@pytest.mark.web
@pytest.mark.web_users
@pytest.mark.full
class TestUsersWeb:

    @pytest.mark.basic
    def test_successful_user_registration_web(self, driver):
        """
        Should register a new user successfully via the web interface.
        """
        fixture_key = create_fixture_key()
        create_user_via_web(driver, fixture_key)
        login_user_via_web(driver, fixture_key)
        delete_user_via_web(driver, fixture_key)
        delete_fixture_data(fixture_key)

    @pytest.mark.basic
    def test_successful_login_web(self, driver):
        """
        Should log in with valid credentials and display the home page.
        """
        fixture_key = create_fixture_key()
        create_user_via_web(driver, fixture_key)
        login_user_via_web(driver, fixture_key)
        home_page = HomePage(driver)
        home_page.goto(BASE_URL)
        home_page.expect_logged_area_visible()
        home_page.expect_add_note_visible()
        try:
            home_page.expect_empty_notes_message()
        except Exception:
            pass
        delete_user_via_web(driver, fixture_key)
        delete_fixture_data(fixture_key)

    @pytest.mark.basic
    def test_profile_data_validation_web(self, driver):
        """
        Should display correct user profile data after login.
        """
        fixture_key = create_fixture_key()
        create_user_via_web(driver, fixture_key)
        login_user_via_web(driver, fixture_key)
        profile_page = ProfilePage(driver)
        profile_page.goto(BASE_URL)
        profile_page.expect_loaded()
        fixture = read_fixture_data(fixture_key)
        # Use only Page Object methods and fixture dict, no hardcoded keys
        profile_page.expect_profile_matches_fixture(fixture)
        delete_user_via_web(driver, fixture_key)
        delete_fixture_data(fixture_key)

    @pytest.mark.basic
    def test_user_deletion_web(self, driver):
        """
        Should delete a user account via the web interface.
        """
        fixture_key = create_fixture_key()
        create_user_via_web(driver, fixture_key)
        login_user_via_web(driver, fixture_key)
        delete_user_via_web(driver, fixture_key)
        delete_fixture_data(fixture_key)

    @pytest.mark.negative
    def test_register_invalid_email_web(self, driver):
        """
        Should show an error when registering with an invalid email address.
        """
        user = generate_user_data()
        page = RegisterPage(driver)
        page.goto(BASE_URL)
        page.expect_loaded()
        user['user_email'] = '@' + user['user_email']
        page.fill_form_with_confirm_password(user, user['user_password'])
        page.submit()
        page.expect_alert_message_for_invalid_email()

    @pytest.mark.negative
    def test_register_wrong_password_web(self, driver):
        """
        Should show an error when password and confirmation do not match during registration.
        """
        user = generate_user_data()
        page = RegisterPage(driver)
        page.goto(BASE_URL)
        page.expect_loaded()
        page.fill_form_with_confirm_password(user, 'e' + user['user_password'])
        page.submit()
        # Use only the Page Object's alert_message selector, no hardcoded XPATH or text
        page.expect_alert_message_for_password_mismatch()

    @pytest.mark.negative
    def test_login_invalid_email_web(self, driver):
        """
        Should show an error when logging in with an invalid email address.
        """
        fixture_key = create_fixture_key()
        create_user_via_web(driver, fixture_key)
        fixture = read_fixture_data(fixture_key)
        page = LoginPage(driver)
        page.goto(BASE_URL)
        page.expect_loaded()
        page.login('e' + fixture['user_email'], fixture['user_password'])
        page.expect_invalid_credentials_alert()
        login_user_via_web(driver, fixture_key)
        delete_user_via_web(driver, fixture_key)
        delete_fixture_data(fixture_key)

    @pytest.mark.negative
    def test_login_wrong_password_web(self, driver):
        """
        Should show an error when logging in with a wrong password.
        """
        fixture_key = create_fixture_key()
        create_user_via_web(driver, fixture_key)
        fixture = read_fixture_data(fixture_key)
        page = LoginPage(driver)
        page.goto(BASE_URL)
        page.expect_loaded()
        page.login(fixture['user_email'], 'e' + fixture['user_password'])
        page.expect_invalid_credentials_alert()
        login_user_via_web(driver, fixture_key)
        delete_user_via_web(driver, fixture_key)
        delete_fixture_data(fixture_key)

    @pytest.mark.basic
    def test_logout_user_web(self, driver):
        """
        Should log out the user and return to the login page.
        """
        fixture_key = create_fixture_key()
        create_user_via_web(driver, fixture_key)
        login_user_via_web(driver, fixture_key)
        home_page = HomePage(driver)
        login_page = LoginPage(driver)
        home_page.goto(BASE_URL)
        home_page.logout()
        login_page.expect_login_link_visible()
        login_user_via_web(driver, fixture_key)
        delete_user_via_web(driver, fixture_key)
        delete_fixture_data(fixture_key)

    @pytest.mark.basic
    def test_update_profile_web(self, driver):
        """
        Should update user profile information (phone, company) via the web interface.
        """
        fixture_key = create_fixture_key()
        create_user_via_web(driver, fixture_key)
        login_user_via_web(driver, fixture_key)
        profile_page = ProfilePage(driver)
        profile_page.goto(BASE_URL)
        profile_page.expect_loaded()
        new_phone = '11999999999'
        new_company = 'Copilot Teste Ltda'
        profile_page.update_profile(new_phone, new_company)
        profile_page.expect_profile_updated()
        delete_user_via_web(driver, fixture_key)
        delete_fixture_data(fixture_key)

    @pytest.mark.negative
    def test_update_profile_invalid_company_web(self, driver):
        """
        Should show an error when updating profile with invalid company name.
        """
        fixture_key = create_fixture_key()
        create_user_via_web(driver, fixture_key)
        login_user_via_web(driver, fixture_key)
        profile_page = ProfilePage(driver)
        profile_page.goto(BASE_URL)
        profile_page.expect_loaded()
        profile_page.update_profile('11999999999', 'e')
        profile_page.expect_company_validation_error()
        delete_user_via_web(driver, fixture_key)
        delete_fixture_data(fixture_key)

    @pytest.mark.negative
    def test_update_profile_invalid_phone_web(self, driver):
        """
        Should show an error when updating profile with invalid phone number.
        """
        fixture_key = create_fixture_key()
        create_user_via_web(driver, fixture_key)
        login_user_via_web(driver, fixture_key)
        profile_page = ProfilePage(driver)
        profile_page.goto(BASE_URL)
        profile_page.expect_loaded()
        profile_page.update_profile('123', 'Copilot Teste Ltda')
        profile_page.expect_phone_validation_error()
        delete_user_via_web(driver, fixture_key)
        delete_fixture_data(fixture_key)

    @pytest.mark.basic
    def test_change_password_web(self, driver):
        """
        Should change the user password via the web interface.
        """
        fixture_key = create_fixture_key()
        create_user_via_web(driver, fixture_key)
        login_user_via_web(driver, fixture_key)
        profile_page = ProfilePage(driver)
        profile_page.goto(BASE_URL)
        profile_page.expect_loaded()
        fixture = read_fixture_data(fixture_key)
        new_password = generate_password()
        profile_page.open_change_password()
        profile_page.change_password(fixture['user_password'], new_password, new_password)
        profile_page.expect_password_updated()
        delete_user_via_web(driver, fixture_key)
        delete_fixture_data(fixture_key)

    @pytest.mark.negative
    def test_change_password_wrong_current_web(self, driver):
        """
        Should show an error when changing password with wrong current password.
        """
        fixture_key = create_fixture_key()
        create_user_via_web(driver, fixture_key)
        login_user_via_web(driver, fixture_key)
        profile_page = ProfilePage(driver)
        profile_page.goto(BASE_URL)
        profile_page.expect_loaded()
        fixture = read_fixture_data(fixture_key)
        new_password = generate_password()
        profile_page.open_change_password()
        profile_page.change_password('e' + fixture['user_password'], new_password, new_password)
        profile_page.expect_current_password_incorrect()
        delete_user_via_web(driver, fixture_key)
        delete_fixture_data(fixture_key)

