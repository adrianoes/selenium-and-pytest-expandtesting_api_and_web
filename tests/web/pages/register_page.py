from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RegisterPage:

    URL = "/notes/app/register"

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.tip_text = (By.XPATH, "//*[contains(text(), 'Using a valid email address is highly recommended')]")
        self.email_input = (By.CSS_SELECTOR, '[data-testid="register-email"]')
        self.name_input = (By.CSS_SELECTOR, '[data-testid="register-name"]')
        self.password_input = (By.CSS_SELECTOR, '[data-testid="register-password"]')
        self.confirm_password_input = (By.CSS_SELECTOR, '[data-testid="register-confirm-password"]')
        self.register_submit_button = (By.CSS_SELECTOR, '[data-testid="register-submit"]')
        self.success_message = (By.XPATH, "//*[contains(text(), 'User account created successfully')]")
        self.alert_message = (By.CSS_SELECTOR, '[data-testid="alert-message"]')

    def expect_alert_message_for_invalid_email(self):
        """
        Assert that the alert message for invalid email is visible.
        """
        alert = self.wait.until(EC.visibility_of_element_located(self.alert_message))
        assert 'valid email address' in alert.text or 'email' in alert.text.lower()

    def expect_alert_message_for_password_mismatch(self):
        """
        Assert that the inline feedback for password mismatch is visible.
        """
        feedback = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'invalid-feedback') and contains(.,'Passwords don')]"))
        )
        assert feedback.is_displayed()

    def goto(self, base_url: str):
        print(f"[RegisterPage.goto] self.URL = {self.URL}")
        url = base_url + self.URL
        print(f"[RegisterPage.goto] Navigating to: {url}")
        self.driver.get(url)
        print(f"[RegisterPage.goto] Navigated to: {self.driver.current_url}")

    def expect_loaded(self):
        assert "/notes/app/register" in self.driver.current_url
        assert self.wait.until(EC.visibility_of_element_located(self.tip_text))

    def fill_form(self, user):
        self.wait.until(EC.visibility_of_element_located(self.email_input)).send_keys(user['user_email'])
        self.wait.until(EC.visibility_of_element_located(self.name_input)).send_keys(user['user_name'])
        self.wait.until(EC.visibility_of_element_located(self.password_input)).send_keys(user['user_password'])
        self.wait.until(EC.visibility_of_element_located(self.confirm_password_input)).send_keys(user['user_password'])

    def submit(self):
        self.wait.until(EC.element_to_be_clickable(self.register_submit_button)).click()

    def fill_form_with_confirm_password(self, user, confirm_password):
        self.wait.until(EC.visibility_of_element_located(self.email_input)).send_keys(user['user_email'])
        self.wait.until(EC.visibility_of_element_located(self.name_input)).send_keys(user['user_name'])
        self.wait.until(EC.visibility_of_element_located(self.password_input)).send_keys(user['user_password'])
        self.wait.until(EC.visibility_of_element_located(self.confirm_password_input)).send_keys(confirm_password)

    def expect_success(self):
        assert "/notes/app/register" in self.driver.current_url
        assert self.wait.until(EC.visibility_of_element_located(self.success_message))

    def expect_alert_message(self, message: str):
        alert = self.wait.until(EC.visibility_of_element_located(self.alert_message))
        assert message in alert.text
