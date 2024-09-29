from    selenium  import  webdriver
import  pytest

@pytest.mark.health
def test_health():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://practice.expandtesting.com/notes/app/")
    assert driver.title == "Notes React Application for Automation Testing Practice"
    driver.quit()