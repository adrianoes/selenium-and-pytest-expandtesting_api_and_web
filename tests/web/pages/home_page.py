from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:
    URL = "/notes/app"

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.welcome_title = (By.XPATH, '//h1[contains(text(), "Welcome to Notes App")]')
        self.create_account_button = (By.CSS_SELECTOR, '[data-testid="open-register-view"]')
        self.add_note_button = (By.CSS_SELECTOR, '[data-testid="add-new-note"]')
        self.notes_list = (By.CSS_SELECTOR, '[data-testid="notes-list"]')
        self.note_cards = (By.CSS_SELECTOR, '[data-testid="note-card"]')
        self.empty_notes_message = (
            By.XPATH,
            "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'dont have any notes') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'do not have any notes')]"
        )
        self.profile_button = (By.CSS_SELECTOR, '[data-testid="profile"]')
        self.logout_button = (By.CSS_SELECTOR, '[data-testid="logout"]')

    def goto(self, base_url: str):
        self.driver.get(base_url + self.URL)

    def expect_welcome_visible(self):
        assert self.wait.until(EC.visibility_of_element_located(self.welcome_title))

    def click_create_account(self):
        self.wait.until(EC.element_to_be_clickable(self.create_account_button)).click()

    def click_add_note(self):
        self.wait.until(EC.element_to_be_clickable(self.add_note_button)).click()

    def expect_notes_list_visible(self):
        assert self.wait.until(EC.visibility_of_element_located(self.notes_list))

    def note_card_by_title(self, title: str):
        cards = self.driver.find_elements(*self.note_cards)
        for card in cards:
            title_elem = card.find_element(By.CSS_SELECTOR, '[data-testid="note-card-title"]')
            if title in title_elem.text:
                return card
        return None

    def note_card_title(self, card):
        return card.find_element(By.CSS_SELECTOR, '[data-testid="note-card-title"]')

    def note_card_description(self, card):
        return card.find_element(By.CSS_SELECTOR, '[data-testid="note-card-description"]')

    def note_card_updated_at(self, card):
        return card.find_element(By.CSS_SELECTOR, '[data-testid="note-card-updated-at"]')

    def note_card_toggle_switch(self, card):
        return card.find_element(By.CSS_SELECTOR, '[data-testid="toggle-note-switch"]')

    def click_view_by_title(self, title: str):
        card = self.note_card_by_title(title)
        if card:
            view_btn = card.find_element(By.CSS_SELECTOR, '[data-testid="note-view"]')
            # Scroll extra na página para garantir visibilidade
            body = self.driver.find_element(By.TAG_NAME, "body")
            for _ in range(15):
                body.send_keys("\ue00f")  # Keys.DOWN
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_btn)
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="note-view"]')))
            view_btn.click()

    def expect_logged_area_visible(self):
        assert self.wait.until(EC.visibility_of_element_located(self.profile_button))
        assert self.wait.until(EC.visibility_of_element_located(self.logout_button))

    def expect_add_note_visible(self):
        assert self.wait.until(EC.visibility_of_element_located(self.add_note_button))

    def expect_empty_notes_message(self):
        assert self.wait.until(EC.visibility_of_element_located(self.empty_notes_message))

    def logout(self):
        self.wait.until(EC.element_to_be_clickable(self.logout_button)).click()

    def go_to_profile(self):
        self.wait.until(EC.element_to_be_clickable(self.profile_button)).click()
        if "/notes/app/profile" not in self.driver.current_url:
            self.driver.get(self.driver.current_url.split('/notes/app')[0] + '/notes/app/profile')
