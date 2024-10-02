
from selenium import webdriver
import requests
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
# options.add_argument('--headless')
# driver = webdriver.Chrome(options=options)
# driver.maximize_window()

def test_sr():

    r = requests.get("https://practice.expandtesting.com/notes/app/register")
    print(r.status_code)
    