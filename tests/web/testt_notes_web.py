import pytest
from tests.support.web_helpers import create_user_via_web, login_user_via_web, delete_user_via_web
from tests.support.test_utils import create_fixture_key, delete_fixture_data
from conftest import BASE_URL
from tests.web.pages.home_page import HomePage
from tests.web.pages.note_modal_page import NoteModalPage
from tests.web.pages.note_details_page import NoteDetailsPage
from tests.data.faker_manager import generate_note_data


@pytest.mark.web
@pytest.mark.web_notes
@pytest.mark.full
class TestNotesWeb:
    def test_create_note_web_invalid_title_and_description(self, driver):
        """
        Should display error messages for invalid title and description when creating a note.
        """
        fixture_key = create_fixture_key()
        create_user_via_web(driver, fixture_key)
        login_user_via_web(driver, fixture_key)
        home_page = HomePage(driver)
        note_modal = NoteModalPage(driver)

        # Só navega para home após login
        home_page.goto(BASE_URL)
        home_page.expect_logged_area_visible()
        home_page.click_add_note()
        note_modal.expect_add_modal_visible()
        invalid_note = {"title": "e", "description": "e", "category": "General"}
        note_modal.fill_and_submit(invalid_note)
        assert note_modal.invalid_title_message_visible()
        assert note_modal.invalid_description_message_visible()
        delete_user_via_web(driver, fixture_key)
        delete_fixture_data(fixture_key)

    @pytest.mark.basic
    def test_create_note_web(self, driver):
        """
        Should create a new note via the web interface and validate its presence in the list and details.
        """
        fixture_key = create_fixture_key()
        create_user_via_web(driver, fixture_key)
        login_user_via_web(driver, fixture_key)
        home_page = HomePage(driver)
        note_modal = NoteModalPage(driver)

        # Só navega para home após login
        home_page.goto(BASE_URL)
        home_page.expect_logged_area_visible()
        home_page.click_add_note()
        note_modal.expect_add_modal_visible()
        note_data = generate_note_data()
        note_modal.fill_and_submit(note_data)
        home_page.expect_notes_list_visible()
        card = home_page.note_card_by_title(note_data['title'])
        assert card is not None
        assert note_data['title'] in home_page.note_card_title(card).text
        assert note_data['description'] in home_page.note_card_description(card).text
        delete_user_via_web(driver, fixture_key)
        delete_fixture_data(fixture_key)

    @pytest.mark.basic
    def test_update_note_web(self, driver):
        """
        Should update a note via the web interface and validate the updated data in the list.
        """
        fixture_key = create_fixture_key()
        create_user_via_web(driver, fixture_key)
        login_user_via_web(driver, fixture_key)
        home_page = HomePage(driver)
        note_modal = NoteModalPage(driver)
        note_details = NoteDetailsPage(driver)

        # Só navega para home após login
        home_page.goto(BASE_URL)
        home_page.expect_logged_area_visible()

        # Cria nota inicial
        home_page.click_add_note()
        note_modal.expect_add_modal_visible()
        note_data = generate_note_data()
        note_modal.fill_and_submit(note_data)
        home_page.expect_notes_list_visible()
        card = home_page.note_card_by_title(note_data['title'])
        assert card is not None
        assert note_data['title'] in home_page.note_card_title(card).text
        assert note_data['description'] in home_page.note_card_description(card).text

        # Edita a nota
        home_page.click_view_by_title(note_data['title'])
        note_details.expect_loaded()
        note_details.open_edit_modal()
        note_modal.expect_edit_modal_visible()
        updated_note = generate_note_data()
        note_modal.fill_and_submit(updated_note)
        home_page.goto(BASE_URL)
        home_page.expect_notes_list_visible()
        updated_card = home_page.note_card_by_title(updated_note['title'])
        assert updated_card is not None
        assert updated_note['title'] in home_page.note_card_title(updated_card).text
        assert updated_note['description'] in home_page.note_card_description(updated_card).text

        delete_user_via_web(driver, fixture_key)
        delete_fixture_data(fixture_key)

    