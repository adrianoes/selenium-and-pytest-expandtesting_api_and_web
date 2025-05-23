import json
# import os
import time
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
from .support_api_and_web import create_user_api, delete_json_file, delete_user_api, login_user_web, login_user_api_getting_id, login_user_api

def test_create_user_api_and_web(driver):
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    user_email = Faker().company_email().replace("-", "")
    user_name = Faker().name()
    user_password = Faker().password(length=12, special_chars=False, digits=True, upper_case=True, lower_case=True)
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
    login_user_api_getting_id(randomData)
    delete_user_api(randomData)
    delete_json_file(randomData)
    time.sleep(5)

def test_login_user_api_and_web(driver):
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
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
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".btn.btn-outline-danger")))
    user_logged = driver.find_element(By.CSS_SELECTOR, ".btn.btn-outline-danger").is_displayed()
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
    delete_user_api(randomData)
    delete_json_file(randomData)
    time.sleep(5)

def test_login_user_api_and_web_invalid_email(driver):
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_email = data['user_email']   
    user_password = data['user_password']  
    user_name = data['user_name']
    driver.get("https://practice.expandtesting.com/notes/app/login")
    for x in range(5):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
    driver.find_element(By.CSS_SELECTOR, "#email").send_keys('@'+user_email)
    driver.find_element(By.CSS_SELECTOR, "#password").send_keys(user_password)
    for x in range(8):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
    driver.find_element(By.CSS_SELECTOR, "div.form-group > button").click()
    driver.implicitly_wait(2)
    invalid_email_message = driver.find_element(By.XPATH,"//div[@data-testid='alert-message'][contains(.,'A valid email address is required')]").is_displayed()
    assert invalid_email_message == True
    login_user_api(randomData)
    delete_user_api(randomData)
    delete_json_file(randomData)
    time.sleep(5)

def test_login_user_api_and_web_wrong_password(driver):
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_email = data['user_email']   
    user_password = data['user_password']  
    user_name = data['user_name']
    driver.get("https://practice.expandtesting.com/notes/app/login")
    for x in range(5):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
    driver.find_element(By.CSS_SELECTOR, "#email").send_keys(user_email)
    driver.find_element(By.CSS_SELECTOR, "#password").send_keys('@'+user_password)
    for x in range(8):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
    driver.find_element(By.CSS_SELECTOR, "div.form-group > button").click()
    driver.implicitly_wait(2)
    invalid_email_message = driver.find_element(By.XPATH,"//div[@data-testid='alert-message'][contains(.,'Incorrect email address or password')]").is_displayed()
    assert invalid_email_message == True
    login_user_api(randomData)
    delete_user_api(randomData)
    delete_json_file(randomData)
    time.sleep(5)

def test_check_user_api_and_web(driver):
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
    login_user_web(randomData, driver)
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
    delete_user_api(randomData)
    delete_json_file(randomData)
    time.sleep(5)

def test_update_user_api_and_web(driver):
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
    login_user_web(randomData, driver)
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
    driver.implicitly_wait(2)
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
    delete_user_api(randomData)
    delete_json_file(randomData)
    time.sleep(5)

def test_update_user_api_and_web_ivalid_company_name(driver):
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
    login_user_web(randomData, driver)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_email = data['user_email']
    user_id = data['user_id']  
    user_name = data['user_name'] 
    user_company = "e"
    user_phone = Faker().bothify(text='############')
    driver.get("https://practice.expandtesting.com/notes/app/profile")
    for x in range(5):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)        
    driver.find_element(By.NAME, "phone").send_keys(user_phone)
    driver.find_element(By.NAME, "company").send_keys(user_company)
    for x in range(12):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN) 
    driver.find_element(By.CSS_SELECTOR, "button[class='btn btn-outline-primary']").click()
    driver.implicitly_wait(2)
    ivalid_company_message = driver.find_element(By.XPATH, "//div[@class='invalid-feedback'][contains(.,'company name should be between 4 and 30 characters')]").is_displayed()
    assert ivalid_company_message == True
    delete_user_api(randomData)
    delete_json_file(randomData)
    time.sleep(5)

def test_update_user_api_and_web_ivalid_phone_number(driver):
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
    login_user_web(randomData, driver)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_email = data['user_email']
    user_id = data['user_id']  
    user_name = data['user_name'] 
    user_company = Faker().company()
    user_phone = "1234"
    driver.get("https://practice.expandtesting.com/notes/app/profile")
    for x in range(5):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)        
    driver.find_element(By.NAME, "phone").send_keys(user_phone)
    driver.find_element(By.NAME, "company").send_keys(user_company)
    for x in range(12):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN) 
    driver.find_element(By.CSS_SELECTOR, "button[class='btn btn-outline-primary']").click()
    driver.implicitly_wait(2)
    ivalid_phone_message = driver.find_element(By.XPATH, "//div[@class='invalid-feedback'][contains(.,'Phone number should be between 8 and 20 digits')]").is_displayed()
    assert ivalid_phone_message == True
    delete_user_api(randomData)
    delete_json_file(randomData)
    time.sleep(5)

def test_update_user_password_api_and_web(driver):
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
    login_user_web(randomData, driver)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_password = data['user_password']
    user_new_password = Faker().password(length=12, special_chars=False, digits=True, upper_case=True, lower_case=True)
    driver.get("https://practice.expandtesting.com/notes/app/profile")
    driver.find_element(By.XPATH, "//button[normalize-space()='Change password']").click()
    driver.find_element(By.CSS_SELECTOR, "input[name='currentPassword']").send_keys(user_password)
    driver.find_element(By.CSS_SELECTOR, "input[name='newPassword']").send_keys(user_new_password)
    driver.find_element(By.CSS_SELECTOR, "input[name='confirmPassword']").send_keys(user_new_password)
    for x in range(10):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN) 
    driver.find_element(By.XPATH, "//button[normalize-space()='Update password']").click()
    driver.implicitly_wait(2)
    user_password_updated = driver.find_element(By.CSS_SELECTOR, "div[class='d-flex']").is_displayed()
    assert user_password_updated == True
    delete_user_api(randomData)
    delete_json_file(randomData)
    time.sleep(5)

def test_update_user_password_api_and_web_same_password(driver):
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
    login_user_web(randomData, driver)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_password = data['user_password']
    driver.get("https://practice.expandtesting.com/notes/app/profile")
    driver.find_element(By.XPATH, "//button[normalize-space()='Change password']").click()
    driver.find_element(By.CSS_SELECTOR, "input[name='currentPassword']").send_keys(user_password)
    driver.find_element(By.CSS_SELECTOR, "input[name='newPassword']").send_keys(user_password)
    driver.find_element(By.CSS_SELECTOR, "input[name='confirmPassword']").send_keys(user_password)
    for x in range(10):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN) 
    driver.find_element(By.XPATH, "//button[normalize-space()='Update password']").click()
    driver.implicitly_wait(2)
    same_password_message = driver.find_element(By.XPATH, "//div[@class='toast-body'][contains(.,'The new password should be different from the current password')]").is_displayed()
    assert same_password_message == True
    delete_user_api(randomData)
    delete_json_file(randomData)
    time.sleep(5)

def test_logout_user_api_and_web(driver):
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
    login_user_web(randomData, driver)
    driver.get("https://practice.expandtesting.com/notes/app/profile")
    driver.find_element(By.XPATH, "//button[normalize-space()='Logout']").click()
    for x in range(10):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)        
    user_logged_out = driver.find_element(By.XPATH, "//a[normalize-space()='Login']").is_displayed()
    assert user_logged_out == True
    login_user_api(randomData)
    delete_user_api(randomData)
    delete_json_file(randomData)
    time.sleep(5)

def test_delete_user_api_and_web(driver):
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
    login_user_web(randomData, driver)
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

# def delete_user_web(driver):
#     driver.get("https://practice.expandtesting.com/notes/app/profile")
#     for x in range(12):
#         driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
#     driver.find_element(By.CSS_SELECTOR, "div.row > div > button").click()
#     driver.find_element(By.CSS_SELECTOR, "div.modal-footer > button.btn.btn-danger").click()
#     driver.implicitly_wait(5)
#     user_deleted = driver.find_element(By.CSS_SELECTOR, "#root > div > div > div > div > div:nth-child(2) > div > div > div").is_displayed()
#     assert user_deleted == True

# def create_user_web(randomData, driver):
#     user_email = Faker().company_email().replace("-", "")
#     user_name = Faker().name()
#     user_password = Faker().password(length=12, special_chars=False, digits=True, upper_case=True, lower_case=True)
#     driver.get("https://practice.expandtesting.com/notes/app/register")
#     driver.find_element(By.CSS_SELECTOR, "#root > div > div > div").click()
#     assert driver.title == "Notes React Application for Automation Testing Practice"
#     driver.find_element(By.CSS_SELECTOR, "#email").send_keys(user_email)
#     driver.find_element(By.CSS_SELECTOR, "#password").send_keys(user_password)
#     driver.find_element(By.CSS_SELECTOR, "#confirmPassword").send_keys(user_password)
#     driver.find_element(By.CSS_SELECTOR, "#name").send_keys(user_name)
#     for x in range(10):
#         driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
#     driver.find_element(By.CSS_SELECTOR, "div.form-group > button").click()
#     driver.implicitly_wait(2)
#     user_created = driver.find_element(By.CSS_SELECTOR, "div.alert.alert-success > b").is_displayed()
#     assert user_created == True
#     combined_responses = {
#         'user_email': user_email,
#         'user_name': user_name,
#         'user_password': user_password
#     }
#     with open(f"./tests/fixtures/file-{randomData}.json", 'w') as json_file:
#         json.dump(combined_responses, json_file, indent=4)

# def login_user_web(randomData, driver):
#     with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
#         data = json.load(json_file)
#     user_email = data['user_email']   
#     user_password = data['user_password']  
#     user_name = data['user_name']
#     driver.get("https://practice.expandtesting.com/notes/app/login")
#     for x in range(5):
#         driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
#     driver.find_element(By.CSS_SELECTOR, "#email").send_keys(user_email)
#     driver.find_element(By.CSS_SELECTOR, "#password").send_keys(user_password)
#     for x in range(8):
#         driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
#     driver.find_element(By.CSS_SELECTOR, "div.form-group > button").click()
#     WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".btn.btn-outline-danger")))
#     user_logged = driver.find_element(By.CSS_SELECTOR, ".btn.btn-outline-danger").is_displayed()
#     assert user_logged == True
#     user_token = driver.execute_script("return localStorage.getItem('token')")
#     headers = {'accept': 'application/json', 'x-auth-token': user_token}
#     resp = requests.get("https://practice.expandtesting.com/notes/api/users/profile", headers=headers)
#     respJS = resp.json()
#     user_id = respJS['data']['id']
#     combined_responses = {
#         'user_email': user_email,
#         'user_id': user_id,
#         'user_name': user_name,
#         'user_password': user_password,
#         'user_token': user_token
#     }
#     with open(f"./tests/fixtures/file-{randomData}.json", 'w') as json_file:
#         json.dump(combined_responses, json_file, indent=4)

# def create_user_api(randomData):
#     user_email = Faker().company_email().replace("-", "")
#     user_name = Faker().name()
#     user_password = Faker().password(length=12, special_chars=False, digits=True, upper_case=True, lower_case=True)
#     body = {'confirmPassword': user_password, 'email': user_email, 'name': user_name, 'password': user_password}
#     headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
#     resp = requests.post("https://practice.expandtesting.com/notes/api/users/register", headers=headers, data=body)
#     respJS = resp.json()
#     assert True == respJS['success']
#     assert 201 == respJS['status']
#     assert "User account created successfully" == respJS['message']
#     assert user_email == respJS['data']['email']
#     assert user_name == respJS['data']['name']
#     user_id = respJS['data']['id']
#     combined_responses = {
#         'user_email': user_email,
#         'user_id': user_id,
#         'user_name': user_name,
#         'user_password': user_password
#     }
#     with open(f"./tests/fixtures/file-{randomData}.json", 'w') as json_file:
#         json.dump(combined_responses, json_file, indent=4)

# def login_user_api_getting_id(randomData):
#     # Getting user id here because there is no way to get in the web user creation test, and we need user id to assert the response.
#     with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
#         data = json.load(json_file)
#     user_email = data['user_email']
#     # user_id = data['user_id']    
#     user_password = data['user_password']  
#     user_name = data['user_name']  
#     body = {'email': user_email, 'password': user_password}
#     headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
#     resp = requests.post("https://practice.expandtesting.com/notes/api/users/login", headers=headers, data=body)
#     respJS = resp.json()
#     assert True == respJS['success']
#     assert 200 == respJS['status']
#     assert "Login successful" == respJS['message']
#     assert user_email == respJS['data']['email']
#     user_id = respJS['data']['id']
#     assert user_name == respJS['data']['name']
#     user_token = respJS['data']['token']
#     combined_responses = {
#         'user_email': user_email,
#         'user_id': user_id,
#         'user_name': user_name,
#         'user_password': user_password,
#         'user_token': user_token
#     }
#     with open(f"./tests/fixtures/file-{randomData}.json", 'w') as json_file:
#         json.dump(combined_responses, json_file, indent=4)
    
# def delete_user_api(randomData):
#     with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
#         data = json.load(json_file)
#     user_token = data['user_token']
#     headers = {'accept': 'application/json', 'x-auth-token': user_token}
#     resp = requests.delete("https://practice.expandtesting.com/notes/api/users/delete-account", headers=headers)
#     respJS = resp.json()
#     assert True == respJS['success']
#     assert 200 == respJS['status']
#     assert "Account successfully deleted" == respJS['message']

# def login_user_api(randomData):
#     with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
#         data = json.load(json_file)
#     user_email = data['user_email']
#     user_id = data['user_id']    
#     user_password = data['user_password']  
#     user_name = data['user_name']  
#     body = {'email': user_email, 'password': user_password}
#     headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
#     resp = requests.post("https://practice.expandtesting.com/notes/api/users/login", headers=headers, data=body)
#     respJS = resp.json()
#     assert True == respJS['success']
#     assert 200 == respJS['status']
#     assert "Login successful" == respJS['message']
#     assert user_email == respJS['data']['email']
#     assert user_id == respJS['data']['id']
#     assert user_name == respJS['data']['name']
#     user_token = respJS['data']['token']
#     combined_responses = {
#         'user_email': user_email,
#         'user_id': user_id,
#         'user_name': user_name,
#         'user_password': user_password,
#         'user_token': user_token
#     }
#     with open(f"./tests/fixtures/file-{randomData}.json", 'w') as json_file:
#         json.dump(combined_responses, json_file, indent=4)

# def delete_json_file(randomData):
#     os.remove(f"./tests/fixtures/file-{randomData}.json")





