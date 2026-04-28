from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from tests.web.pages.register_page import RegisterPage
from tests.web.pages.login_page import LoginPage
from tests.web.pages.home_page import HomePage
from tests.web.pages.profile_page import ProfilePage
from tests.data.faker_manager import generate_user_data
from tests.support.test_utils import save_fixture_data, read_fixture_data
from conftest import BASE_URL

def create_user_via_web(driver: WebDriver, fixture_key: str):
    import json
    from tests.data.faker_manager import generate_user_data
    from tests.support.test_utils import save_fixture_data
    user = generate_user_data()
    page = RegisterPage(driver)
    # Navega explicitamente para a página de registro usando o método do Page Object
    page.goto(BASE_URL)
    page.expect_loaded()
    page.fill_form(user)
    page.submit()
    try:
        page.wait.until(EC.visibility_of_element_located(page.success_message))
    except Exception:
        page.wait.until(EC.visibility_of_element_located(page.alert_message))
    save_fixture_data(fixture_key, user)

def login_user_via_web(driver: WebDriver, fixture_key: str):
    import json
    import requests
    from tests.support.test_utils import read_fixture_data, save_fixture_data
    data = read_fixture_data(fixture_key)
    user_email = data['user_email']
    user_password = data['user_password']
    page = LoginPage(driver)
    # Navega explicitamente para a página de login usando o método do Page Object
    page.goto(BASE_URL)
    page.expect_loaded()
    page.login(user_email, user_password)
    home_page = HomePage(driver)
    home_page.wait.until(EC.visibility_of_element_located(home_page.logout_button))
    user_token = driver.execute_script("return localStorage.getItem('token')")
    headers = {'accept': 'application/json', 'x-auth-token': user_token}
    resp = requests.get(f"{BASE_URL}/notes/api/users/profile", headers=headers)
    respJS = resp.json()
    user_id = respJS['data']['id']
    data.update({'user_id': user_id, 'user_token': user_token})
    save_fixture_data(fixture_key, data)

def go_to_home(driver: WebDriver):
    home_page = HomePage(driver)
    home_page.goto(BASE_URL)
    home_page.expect_welcome_visible()
    return home_page

def go_to_profile(driver: WebDriver):
    profile_page = ProfilePage(driver)
    profile_page.goto(BASE_URL)
    profile_page.expect_loaded()
    return profile_page

def delete_user_via_web(driver: WebDriver, fixture_key: str):
    page = ProfilePage(driver)
    page.goto(BASE_URL)
    page.expect_loaded()
    page.delete_account()
    page.wait.until(EC.visibility_of_element_located(page.alert_message))


