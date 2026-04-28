from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    URL = "/notes/app/login"

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.login_title = (By.XPATH, '//h1[text()="Login"]')
        self.email_input = (By.CSS_SELECTOR, '[data-testid="login-email"]')
        self.password_input = (By.CSS_SELECTOR, '[data-testid="login-password"]')
        self.login_submit_button = (By.CSS_SELECTOR, '[data-testid="login-submit"]')
        self.account_deleted_message = (By.CSS_SELECTOR, '[data-testid="alert-message"]')
        self.login_link = (By.LINK_TEXT, 'Login')

    def goto(self, base_url: str):
        url = base_url + self.URL
        self.driver.get(url)
        print(f"[LoginPage.goto] Navigated to: {self.driver.current_url}")

    def expect_loaded(self):
        assert "/notes/app/login" in self.driver.current_url
        assert self.wait.until(EC.visibility_of_element_located(self.login_title))

    def login(self, email: str, password: str):
        email_input = self.wait.until(EC.visibility_of_element_located(self.email_input))
        email_input.clear()
        email_input.send_keys(email)
        password_input = self.wait.until(EC.visibility_of_element_located(self.password_input))
        password_input.clear()
        password_input.send_keys(password)
        self.wait.until(EC.element_to_be_clickable(self.login_submit_button)).click()

    def expect_account_deleted_alert(self):
        alert = self.wait.until(EC.visibility_of_element_located(self.account_deleted_message))
        assert "Your account has been deleted. You should create a new account to continue." in alert.text

    def expect_invalid_credentials_alert(self):
        alert = self.wait.until(EC.visibility_of_element_located(self.account_deleted_message))
        assert "Incorrect email address or password" in alert.text

    def expect_login_link_visible(self):
        login_link = self.wait.until(EC.visibility_of_element_located(self.login_link))
        assert login_link.is_displayed()
