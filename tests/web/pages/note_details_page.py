from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NoteDetailsPage:
    URL_PREFIX = "/notes/app/notes/"

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.note_card = (By.CSS_SELECTOR, '[data-testid="note-card"]')
        self.note_title = (By.CSS_SELECTOR, '[data-testid="note-card-title"]')
        self.note_description = (By.CSS_SELECTOR, '[data-testid="note-card-description"]')
        self.note_updated_at = (By.CSS_SELECTOR, '[data-testid="note-card-updated-at"]')
        self.toggle_switch = (By.CSS_SELECTOR, '[data-testid="toggle-note-switch"]')
        self.edit_button = (By.CSS_SELECTOR, '[data-testid="note-edit"]')
        self.delete_button = (By.CSS_SELECTOR, '[data-testid="note-delete"]')
        self.confirm_delete_button = (By.CSS_SELECTOR, '[data-testid="note-delete-confirm"]')

    def goto(self, base_url: str, note_id: str):
        self.driver.get(f"{base_url}{self.URL_PREFIX}{note_id}")

    def expect_loaded(self):
        assert "/notes/app/notes/" in self.driver.current_url
        assert self.wait.until(EC.visibility_of_element_located(self.note_card))

    def get_note_id_from_url(self):
        url = self.driver.current_url
        parts = url.split("/notes/app/notes/")
        return parts[1] if len(parts) > 1 else None

    def expect_title(self, title: str):
        assert title in self.wait.until(EC.visibility_of_element_located(self.note_title)).text

    def expect_description(self, description: str):
        assert description in self.wait.until(EC.visibility_of_element_located(self.note_description)).text

    def expect_updated_at(self):
        updated_at = self.wait.until(EC.visibility_of_element_located(self.note_updated_at)).text.strip()
        assert len(updated_at) > 10
        return updated_at

    def expect_toggle_checked(self, checked: bool):
        toggle = self.wait.until(EC.visibility_of_element_located(self.toggle_switch))
        is_checked = toggle.get_attribute("aria-checked") == "true"
        assert is_checked == checked

    def open_edit_modal(self):
        self.wait.until(EC.element_to_be_clickable(self.edit_button)).click()

    def delete_note(self):
        self.wait.until(EC.element_to_be_clickable(self.delete_button)).click()
        self.wait.until(EC.element_to_be_clickable(self.confirm_delete_button)).click()
