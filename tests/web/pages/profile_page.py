from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

class ProfilePage:
    URL = "/notes/app/profile"

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.profile_settings_title = (By.XPATH, '//h1[contains(text(), "Profile settings")]')
        self.user_id_input = (By.CSS_SELECTOR, '[data-testid="user-id"]')
        self.user_email_input = (By.CSS_SELECTOR, '[data-testid="user-email"]')
        self.user_name_input = (By.CSS_SELECTOR, '[data-testid="user-name"]')
        self.phone_input = (By.CSS_SELECTOR, 'input[name="phone"]')
        self.company_input = (By.CSS_SELECTOR, 'input[name="company"]')
        self.update_profile_button = (By.XPATH, '//button[contains(text(), "Update profile")]')
        self.change_password_button = (By.XPATH, '//button[contains(text(), "Change password")]')
        self.current_password_input = (By.CSS_SELECTOR, '[data-testid="current-password"]')
        self.new_password_input = (By.CSS_SELECTOR, '[data-testid="new-password"]')
        self.confirm_password_input = (By.CSS_SELECTOR, '[data-testid="confirm-password"]')
        self.update_password_button = (By.XPATH, '//button[contains(text(), "Update password")]')
        self.alert_message = (By.CSS_SELECTOR, '[data-testid="alert-message"]')
        self.delete_account_button = (By.CSS_SELECTOR, '[data-testid="delete-account"]')
        self.confirm_delete_button = (By.CSS_SELECTOR, '[data-testid="note-delete-confirm"]')

    def expect_profile_matches_fixture(self, fixture):
        """
        Assert that the profile fields match the fixture data.
        """
        assert self.wait.until(EC.visibility_of_element_located(self.user_id_input)).get_attribute('value') == fixture['user_id']
        assert self.wait.until(EC.visibility_of_element_located(self.user_email_input)).get_attribute('value') == fixture['user_email']
        assert self.wait.until(EC.visibility_of_element_located(self.user_name_input)).get_attribute('value') == fixture['user_name']


    def goto(self, base_url: str):
        self.driver.get(base_url + self.URL)

    def expect_loaded(self):
        assert "/notes/app/profile" in self.driver.current_url
        assert self.wait.until(EC.visibility_of_element_located(self.profile_settings_title))

    def expect_user_data(self, email: str, full_name: str):
        assert self.wait.until(EC.visibility_of_element_located(self.user_email_input)).get_attribute('value') == email
        assert self.wait.until(EC.visibility_of_element_located(self.user_name_input)).get_attribute('value') == full_name

    def expect_user_id(self, user_id: str):
        assert self.wait.until(EC.visibility_of_element_located(self.user_id_input)).get_attribute('value') == user_id

    def update_profile(self, phone: str, company: str):
        self.wait.until(EC.visibility_of_element_located(self.phone_input)).clear()
        self.wait.until(EC.visibility_of_element_located(self.phone_input)).send_keys(phone)
        self.wait.until(EC.visibility_of_element_located(self.company_input)).clear()
        self.wait.until(EC.visibility_of_element_located(self.company_input)).send_keys(company)
        self.wait.until(EC.element_to_be_clickable(self.update_profile_button)).click()

    def expect_profile_updated(self):
        alert = self.wait.until(EC.visibility_of_element_located(self.alert_message))
        assert 'Profile updated successful' in alert.text

    def expect_company_validation_error(self):
        error = self.driver.find_element(By.XPATH, "//*[contains(text(), 'company name should be between 4 and 30 characters')]")
        assert error.is_displayed()

    def expect_phone_validation_error(self):
        error = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Phone number should be between 8 and 20 digits')]")
        assert error.is_displayed()

    def open_change_password(self):
        self.wait.until(EC.element_to_be_clickable(self.change_password_button)).click()

    def change_password(self, current_password: str, new_password: str, confirm_password: str):
        self.wait.until(EC.visibility_of_element_located(self.current_password_input)).send_keys(current_password)
        self.wait.until(EC.visibility_of_element_located(self.new_password_input)).send_keys(new_password)
        self.wait.until(EC.visibility_of_element_located(self.confirm_password_input)).send_keys(confirm_password)
        self.wait.until(EC.element_to_be_clickable(self.update_password_button)).click()

    def expect_password_updated(self):
        alert = self.wait.until(EC.visibility_of_element_located(self.alert_message))
        assert 'The password was successfully updated' in alert.text

    def expect_current_password_incorrect(self):
        alert = self.wait.until(EC.visibility_of_element_located(self.alert_message))
        assert 'The current password is incorrect' in alert.text

    def delete_account(self):
        try:
            self.wait.until_not(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, '.modal, .loader, .backdrop, .MuiBackdrop-root, .snackbar, .toast')))
        except Exception:
            pass
        btn = self.wait.until(EC.presence_of_element_located(self.delete_account_button))
        body = self.driver.find_element(By.CSS_SELECTOR, "body")
        for _ in range(2):
            body.send_keys(Keys.DOWN)
        for _ in range(5):
            if btn.is_displayed():
                break
            body.send_keys(Keys.DOWN)
        try:
            self.wait.until_not(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, '.modal, .loader, .backdrop, .MuiBackdrop-root, .snackbar, .toast')))
        except Exception:
            pass
        btn = self.wait.until(EC.element_to_be_clickable(self.delete_account_button))
        self.driver.save_screenshot('before_delete_click.png')
        clicked = False
        for _ in range(3):
            try:
                btn.click()
                clicked = True
                break
            except Exception:
                pass
        if not clicked:
            self.driver.execute_script("arguments[0].click();", btn)
        confirm_btn = self.wait.until(EC.element_to_be_clickable(self.confirm_delete_button))
        confirm_btn.click()
