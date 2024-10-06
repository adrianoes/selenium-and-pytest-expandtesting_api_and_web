import json
import os
import time
import requests
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument('--headless')
from faker import Faker
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from .support_ui import create_user_ui, delete_json_file, delete_user_ui, login_user_ui
# driver = webdriver.Chrome()
driver = webdriver.Chrome(options=options)
driver.maximize_window()

def test_create_user_ui():
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    user_email = Faker().company_email()
    user_name = Faker().name()
    user_password = Faker().password()
    driver.get("https://practice.expandtesting.com/notes/app/register")
    driver.find_element(By.CSS_SELECTOR, "#root > div > div > div").click()
    assert driver.title == "Notes React Application for Automation Testing Practice"
    driver.find_element(By.CSS_SELECTOR, "#email").send_keys(user_email)
    driver.find_element(By.CSS_SELECTOR, "#password").send_keys(user_password)
    driver.find_element(By.CSS_SELECTOR, "#confirmPassword").send_keys(user_password)
    driver.find_element(By.CSS_SELECTOR, "#name").send_keys(user_name)
    for x in range(10):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
    driver.find_element(By.CSS_SELECTOR, "div.form-group > button").click()
    driver.implicitly_wait(2)
    user_created = driver.find_element(By.CSS_SELECTOR, "div.alert.alert-success > b").is_displayed()
    assert user_created == True
    combined_responses = {
        'user_email': user_email,
        'user_name': user_name,
        'user_password': user_password
    }
    with open(f"./tests/fixtures/file-{randomData}.json", 'w') as json_file:
        json.dump(combined_responses, json_file, indent=4)
    login_user_ui(randomData)
    delete_user_ui()
    delete_json_file(randomData)
    time.sleep(5)

def test_login_user_ui():
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_ui(randomData)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_email = data['user_email']   
    user_password = data['user_password']  
    user_name = data['user_name']
    driver.get("https://practice.expandtesting.com/notes/app/login")
    for x in range(5):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
    driver.find_element(By.CSS_SELECTOR, "#email").send_keys(user_email)
    driver.find_element(By.CSS_SELECTOR, "#password").send_keys(user_password)
    for x in range(8):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
    driver.find_element(By.CSS_SELECTOR, "div.form-group > button").click()
    user_logged = driver.find_element(By.CSS_SELECTOR,"#navbarSupportedContent > ul > li:nth-child(1) > a").is_displayed()
    assert user_logged == True
    user_token = driver.execute_script("return localStorage.getItem('token')")
    headers = {'accept': 'application/json', 'x-auth-token': user_token}
    resp = requests.get("https://practice.expandtesting.com/notes/api/users/profile", headers=headers)
    respJS = resp.json()
    user_id = respJS['data']['id']
    combined_responses = {
        'user_email': user_email,
        'user_id': user_id,
        'user_name': user_name,
        'user_password': user_password,
        'user_token': user_token
    }
    with open(f"./tests/fixtures/file-{randomData}.json", 'w') as json_file:
        json.dump(combined_responses, json_file, indent=4)
    delete_user_ui()
    delete_json_file(randomData)
    time.sleep(5)

def test_check_user_ui():
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_ui(randomData)
    login_user_ui(randomData)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_email = data['user_email']   
    user_id = data['user_id'] 
    user_name = data['user_name'] 
    driver.get("https://practice.expandtesting.com/notes/app/profile")
    for x in range(5):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
    user_id_element = driver.find_element(By.CSS_SELECTOR, "#user-id")     
    user_email_element = driver.find_element(By.CSS_SELECTOR, "#user-email")
    user_name_element = driver.find_element(By.NAME, "name")
    assert user_email == user_email_element.get_attribute("value")
    assert user_id == user_id_element.get_attribute("value")
    assert user_name == user_name_element.get_attribute("value")
    delete_user_ui()
    delete_json_file(randomData)
    time.sleep(5)

def test_update_user_ui():
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_ui(randomData)
    login_user_ui(randomData)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_email = data['user_email']
    user_id = data['user_id']  
    user_name = data['user_name'] 
    user_company = Faker().company()
    user_phone = Faker().bothify(text='############')
    driver.get("https://practice.expandtesting.com/notes/app/profile")
    for x in range(5):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)        
    driver.find_element(By.NAME, "phone").send_keys(user_phone)
    driver.find_element(By.NAME, "company").send_keys(user_company)
    for x in range(12):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN) 
    driver.find_element(By.CSS_SELECTOR, "button[class='btn btn-outline-primary']").click()
    user_updated = driver.find_element(By.CSS_SELECTOR, "div[class='d-flex']").is_displayed()
    assert user_updated == True
    user_company_element = driver.find_element(By.NAME, "company")
    user_email_element = driver.find_element(By.CSS_SELECTOR, "#user-email")
    user_id_element = driver.find_element(By.CSS_SELECTOR, "#user-id")
    user_name_element = driver.find_element(By.NAME, "name")
    user_phone_element = driver.find_element(By.NAME, "phone")
    assert user_company == user_company_element.get_attribute("value")
    assert user_email == user_email_element.get_attribute("value")
    assert user_id == user_id_element.get_attribute("value")
    assert user_name == user_name_element.get_attribute("value")
    assert user_phone == user_phone_element.get_attribute("value")
    delete_user_ui()
    delete_json_file(randomData)
    time.sleep(5)

def test_update_user_password_ui():
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_ui(randomData)
    login_user_ui(randomData)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_password = data['user_password']
    user_new_password = Faker().password()
    driver.get("https://practice.expandtesting.com/notes/app/profile")
    driver.find_element(By.XPATH, "//button[normalize-space()='Change password']").click()
    driver.find_element(By.CSS_SELECTOR, "input[name='currentPassword']").send_keys(user_password)
    driver.find_element(By.CSS_SELECTOR, "input[name='newPassword']").send_keys(user_new_password)
    driver.find_element(By.CSS_SELECTOR, "input[name='confirmPassword']").send_keys(user_new_password)
    for x in range(10):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN) 
    driver.find_element(By.XPATH, "//button[normalize-space()='Update password']").click()
    user_password_updated = driver.find_element(By.CSS_SELECTOR, "div[class='d-flex']").is_displayed()
    assert user_password_updated == True
    delete_user_ui()
    delete_json_file(randomData)
    time.sleep(5)

def test_logout_user_ui():
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_ui(randomData)
    login_user_ui(randomData)
    driver.get("https://practice.expandtesting.com/notes/app/profile")
    driver.find_element(By.XPATH, "//button[normalize-space()='Logout']").click()
    for x in range(10):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)        
    user_logged_out = driver.find_element(By.XPATH, "//a[normalize-space()='Login']").is_displayed()
    assert user_logged_out == True
    login_user_ui(randomData)
    delete_user_ui()
    delete_json_file(randomData)
    time.sleep(5)

def test_delete_user_ui():
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_ui(randomData)
    login_user_ui(randomData)
    driver.get("https://practice.expandtesting.com/notes/app/profile")
    for x in range(12):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
    driver.find_element(By.CSS_SELECTOR, "div.row > div > button").click()
    driver.find_element(By.CSS_SELECTOR, "div.modal-footer > button.btn.btn-danger").click()
    driver.implicitly_wait(5)
    user_deleted = driver.find_element(By.CSS_SELECTOR, "#root > div > div > div > div > div:nth-child(2) > div > div > div").is_displayed()
    assert user_deleted == True
    delete_json_file(randomData)
    time.sleep(5)

def delete_json_file(randomData):
    os.remove(f"./tests/fixtures/file-{randomData}.json")

def create_user_ui(randomData):
    user_email = Faker().company_email()
    user_name = Faker().name()
    user_password = Faker().password()
    driver.get("https://practice.expandtesting.com/notes/app/register")
    driver.find_element(By.CSS_SELECTOR, "#root > div > div > div").click()
    assert driver.title == "Notes React Application for Automation Testing Practice"
    driver.find_element(By.CSS_SELECTOR, "#email").send_keys(user_email)
    driver.find_element(By.CSS_SELECTOR, "#password").send_keys(user_password)
    driver.find_element(By.CSS_SELECTOR, "#confirmPassword").send_keys(user_password)
    driver.find_element(By.CSS_SELECTOR, "#name").send_keys(user_name)
    for x in range(10):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
    driver.find_element(By.CSS_SELECTOR, "div.form-group > button").click()
    driver.implicitly_wait(2)
    user_created = driver.find_element(By.CSS_SELECTOR, "div.alert.alert-success > b").is_displayed()
    assert user_created == True
    combined_responses = {
        'user_email': user_email,
        'user_name': user_name,
        'user_password': user_password
    }
    with open(f"./tests/fixtures/file-{randomData}.json", 'w') as json_file:
        json.dump(combined_responses, json_file, indent=4)

def login_user_ui(randomData):
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_email = data['user_email']   
    user_password = data['user_password']  
    user_name = data['user_name']
    driver.get("https://practice.expandtesting.com/notes/app/login")
    for x in range(5):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
    driver.find_element(By.CSS_SELECTOR, "#email").send_keys(user_email)
    driver.find_element(By.CSS_SELECTOR, "#password").send_keys(user_password)
    for x in range(8):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
    driver.find_element(By.CSS_SELECTOR, "div.form-group > button").click()
    user_logged = driver.find_element(By.CSS_SELECTOR,"#navbarSupportedContent > ul > li:nth-child(1) > a").is_displayed()
    assert user_logged == True
    user_token = driver.execute_script("return localStorage.getItem('token')")
    headers = {'accept': 'application/json', 'x-auth-token': user_token}
    resp = requests.get("https://practice.expandtesting.com/notes/api/users/profile", headers=headers)
    respJS = resp.json()
    user_id = respJS['data']['id']
    combined_responses = {
        'user_email': user_email,
        'user_id': user_id,
        'user_name': user_name,
        'user_password': user_password,
        'user_token': user_token
    }
    with open(f"./tests/fixtures/file-{randomData}.json", 'w') as json_file:
        json.dump(combined_responses, json_file, indent=4)

def delete_user_ui():
    driver.get("https://practice.expandtesting.com/notes/app/profile")
    for x in range(12):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
    driver.find_element(By.CSS_SELECTOR, "div.row > div > button").click()
    driver.find_element(By.CSS_SELECTOR, "div.modal-footer > button.btn.btn-danger").click()
    driver.implicitly_wait(5)
    user_deleted = driver.find_element(By.CSS_SELECTOR, "#root > div > div > div > div > div:nth-child(2) > div > div > div").is_displayed()
    assert user_deleted == True