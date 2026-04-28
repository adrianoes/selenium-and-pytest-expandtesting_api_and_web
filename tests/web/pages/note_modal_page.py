from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NoteModalPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.add_modal_title = (By.XPATH, "//h5[contains(text(), 'Add new note')]")
        self.edit_modal_title = (By.XPATH, "//h5[contains(text(), 'Edit note')]")
        self.category_select = (By.CSS_SELECTOR, '[data-testid="note-category"]')
        self.completed_checkbox = (By.CSS_SELECTOR, '[data-testid="note-completed"]')
        self.title_input = (By.CSS_SELECTOR, '[data-testid="note-title"]')
        self.description_input = (By.CSS_SELECTOR, '[data-testid="note-description"]')
        self.submit_button = (By.CSS_SELECTOR, '[data-testid="note-submit"]')

    def invalid_title_message_visible(self):
        try:
            error = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Title should be between 4 and 100 characters')]")
            return error.is_displayed()
        except Exception:
            return False

    def invalid_description_message_visible(self):
        try:
            error = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Description should be between 4 and 1000 characters')]")
            return error.is_displayed()
        except Exception:
            return False

    def expect_add_modal_visible(self):
        assert self.wait.until(EC.visibility_of_element_located(self.add_modal_title))
        assert self.wait.until(EC.visibility_of_element_located(self.category_select))

    def expect_edit_modal_visible(self):
        assert self.wait.until(EC.visibility_of_element_located(self.edit_modal_title))
        assert self.wait.until(EC.visibility_of_element_located(self.category_select))

    def fill_and_submit(self, note):
        self.wait.until(EC.visibility_of_element_located(self.category_select)).send_keys(note['category'])
        for _ in range(note.get('completed', 0)):
            self.wait.until(EC.element_to_be_clickable(self.completed_checkbox)).click()
        self.wait.until(EC.visibility_of_element_located(self.title_input)).clear()
        self.wait.until(EC.visibility_of_element_located(self.title_input)).send_keys(note['title'])
        self.wait.until(EC.visibility_of_element_located(self.description_input)).clear()
        self.wait.until(EC.visibility_of_element_located(self.description_input)).send_keys(note['description'])
        self.wait.until(EC.element_to_be_clickable(self.submit_button)).click()

    def expect_title_validation_error(self):
        error = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Title should be between 4 and 100 characters')]")
        assert error.is_displayed()

    def expect_description_validation_error(self):
        error = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Description should be between 4 and 1000 characters')]")
        assert error.is_displayed()
