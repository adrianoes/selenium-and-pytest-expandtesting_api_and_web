import time
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument('--headless')
# driver = webdriver.Chrome()
driver = webdriver.Chrome(options=options)
driver.maximize_window()

def test_health():
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get("https://practice.expandtesting.com/notes/app/")
    assert driver.title == "Notes React Application for Automation Testing Practice"
