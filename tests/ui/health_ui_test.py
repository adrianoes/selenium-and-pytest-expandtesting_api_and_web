from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_health(driver):  
    driver.get("https://practice.expandtesting.com/notes/app/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    assert driver.title == "Notes React Application for Automation Testing Practice"
