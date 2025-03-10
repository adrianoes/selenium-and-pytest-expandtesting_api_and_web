import json
import os
import time
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker

def login_user_ui(randomData, driver):
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_email = data['user_email']   
    user_password = data['user_password']  
    user_name = data['user_name']
    driver.get("https://practice.expandtesting.com/notes/app/login")
    for x in range(6):
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

def create_note_ui(randomData, driver):
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file) 
    user_token = data['user_token'] 
    # 1 = Home, 2 = Work , 3 = Personal
    note_category = Faker().random_element(elements=(1, 2, 3))
    # 1 = Checked, 2 = Unchecked
    note_completed = Faker().random_element(elements=(1,2))
    note_description = Faker().sentence(3)
    note_title = Faker().sentence(2)
    driver.get("https://practice.expandtesting.com/notes/app/")
    for x in range(5):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
    time.sleep(5)
    driver.find_element(By.XPATH,"//button[normalize-space()='+ Add Note']").click() 
    driver.find_element(By.CSS_SELECTOR,"#category").click()
    driver.find_element(By.CSS_SELECTOR,f"#category > option:nth-child({note_category})").click()
    for x in range(note_completed):
        driver.find_element(By.CSS_SELECTOR,f"#completed").click()
    driver.find_element(By.CSS_SELECTOR,"#title").send_keys(note_title)
    driver.find_element(By.CSS_SELECTOR,"#description").send_keys(note_description)
    driver.find_element(By.CSS_SELECTOR,"button[data-testid='note-submit']").click()
    for x in range(15):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
    note_view_element = driver.find_element(By.CSS_SELECTOR, 'a[data-testid="note-view"]')
    href_value = note_view_element.get_attribute('href')
    note_id = href_value.split('/')[-1]
    if note_completed == 1:  
        note_message_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f'//div[@data-testid="progress-info" and text()="You have completed all notes"]')))
    else:
        note_message_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f'//div[@data-testid="progress-info" and text()="You have 0/1 notes completed in the all categories"]')))
    note_title_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f'//div[@data-testid="note-card-title" and text()="{note_title}"]')))
    note_description_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//p[@class='card-text' and text()='{note_description}']")))
    note_updated_at_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="note-card-updated-at"]')))
    note_updated_at = note_updated_at_element.text.strip()
    note_style = note_title_element.get_attribute("style")
    if note_completed == 1:
        assert note_style == "background-color: rgba(40, 46, 41, 0.6); color: rgb(255, 255, 255);"
    elif note_category == 1:
        assert note_style == "background-color: rgb(255, 145, 0); color: rgb(255, 255, 255);"
    elif note_category == 2:
         assert note_style == "background-color: rgb(92, 107, 192); color: rgb(255, 255, 255);"
    else:
        assert note_style == "background-color: rgb(50, 140, 160); color: rgb(255, 255, 255);"        
    assert note_description_element.is_displayed()
    assert note_message_element.is_displayed()
    assert note_title_element.is_displayed()
    assert note_updated_at_element.is_displayed()
    combined_responses = {
        'note_category': note_category,
        'note_completed': note_completed,
        'note_description': note_description,
        'note_id': note_id,
        'note_title': note_title,
        'note_updated_at': note_updated_at,
        'user_token': user_token
    }
    with open(f"./tests/fixtures/file-{randomData}.json", 'w') as json_file:
        json.dump(combined_responses, json_file, indent=4)    

def create_user_api(randomData):
    user_email = Faker().company_email().replace("-", "")
    user_name = Faker().name()
    user_password = Faker().password(length=12, special_chars=False, digits=True, upper_case=True, lower_case=True)
    body = {'confirmPassword': user_password, 'email': user_email, 'name': user_name, 'password': user_password}
    print(body)
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    resp = requests.post("https://practice.expandtesting.com/notes/api/users/register", headers=headers, data=body)
    respJS = resp.json()
    print(respJS)
    assert True == respJS['success']
    assert 201 == respJS['status']
    assert "User account created successfully" == respJS['message']
    assert user_email == respJS['data']['email']
    assert user_name == respJS['data']['name']
    user_id = respJS['data']['id']
    combined_responses = {
        'user_email': user_email,
        'user_id': user_id,
        'user_name': user_name,
        'user_password': user_password
    }
    with open(f"./tests/fixtures/file-{randomData}.json", 'w') as json_file:
        json.dump(combined_responses, json_file, indent=4)

def delete_user_api(randomData):
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_token = data['user_token']
    headers = {'accept': 'application/json', 'x-auth-token': user_token}
    resp = requests.delete("https://practice.expandtesting.com/notes/api/users/delete-account", headers=headers)
    respJS = resp.json()
    print(respJS)
    assert True == respJS['success']
    assert 200 == respJS['status']
    assert "Account successfully deleted" == respJS['message']

def delete_note_api(randomData):    
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    note_id = data['note_id']
    user_token = data['user_token']
    headers = {'accept': 'application/json', 'x-auth-token': user_token}
    resp = requests.delete(f"https://practice.expandtesting.com/notes/api/notes/{note_id}", headers=headers)
    respJS = resp.json()
    print(respJS)
    assert True == respJS['success']
    assert 200 == respJS['status']
    assert "Note successfully deleted" == respJS['message']

def login_user_api_getting_id(randomData):
    # Getting user id here because there is no way to get in the ui user creation test, and we need user id to assert the response.
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_email = data['user_email']
    # user_id = data['user_id']    
    user_password = data['user_password']  
    user_name = data['user_name']  
    body = {'email': user_email, 'password': user_password}
    print(body)
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    resp = requests.post("https://practice.expandtesting.com/notes/api/users/login", headers=headers, data=body)
    respJS = resp.json()
    print(respJS)
    assert True == respJS['success']
    assert 200 == respJS['status']
    assert "Login successful" == respJS['message']
    assert user_email == respJS['data']['email']
    user_id = respJS['data']['id']
    assert user_name == respJS['data']['name']
    user_token = respJS['data']['token']
    combined_responses = {
        'user_email': user_email,
        'user_id': user_id,
        'user_name': user_name,
        'user_password': user_password,
        'user_token': user_token
    }
    with open(f"./tests/fixtures/file-{randomData}.json", 'w') as json_file:
        json.dump(combined_responses, json_file, indent=4)

def login_user_api(randomData):
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_email = data['user_email']
    user_id = data['user_id']    
    user_password = data['user_password']  
    user_name = data['user_name']  
    body = {'email': user_email, 'password': user_password}
    print(body)
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    resp = requests.post("https://practice.expandtesting.com/notes/api/users/login", headers=headers, data=body)
    respJS = resp.json()
    print(respJS)
    assert True == respJS['success']
    assert 200 == respJS['status']
    assert "Login successful" == respJS['message']
    assert user_email == respJS['data']['email']
    assert user_id == respJS['data']['id']
    assert user_name == respJS['data']['name']
    user_token = respJS['data']['token']
    combined_responses = {
        'user_email': user_email,
        'user_id': user_id,
        'user_name': user_name,
        'user_password': user_password,
        'user_token': user_token
    }
    with open(f"./tests/fixtures/file-{randomData}.json", 'w') as json_file:
        json.dump(combined_responses, json_file, indent=4)

def delete_json_file(randomData):
    os.remove(f"./tests/fixtures/file-{randomData}.json")