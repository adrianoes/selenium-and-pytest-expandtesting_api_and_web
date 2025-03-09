import json
import os
import requests
from faker import Faker
import time
# from .support_api import create_user_api, delete_json_file, delete_user_api, login_user_api

def test_create_user_api():
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    user_email = Faker().company_email().replace("-", "")
    user_name = Faker().name()
    user_password = Faker().password(length=12, special_chars=False, digits=True, upper_case=True, lower_case=True)
    body = {'confirmPassword': user_password, 'email': user_email, 'name': user_name, 'password': user_password}
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    resp = requests.post("https://practice.expandtesting.com/notes/api/users/register", headers=headers, data=body)
    respJS = resp.json()
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
    login_user_api(randomData)
    delete_user_api(randomData)
    delete_json_file(randomData)
    time.sleep(5)

def test_create_user_api_bad_request():
    user_email = Faker().company_email().replace("-", "")
    user_name = Faker().name()
    user_password = Faker().password(length=12, special_chars=False, digits=True, upper_case=True, lower_case=True)
    body = {'confirmPassword': user_password, 'email': '@'+user_email, 'name': user_name, 'password': user_password}
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    resp = requests.post("https://practice.expandtesting.com/notes/api/users/register", headers=headers, data=body)
    respJS = resp.json()
    assert False == respJS['success']
    assert 400 == respJS['status']
    assert "A valid email address is required" == respJS['message']
    time.sleep(5)

def test_login_user_api():
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_email = data['user_email']
    user_id = data['user_id']    
    user_password = data['user_password']  
    user_name = data['user_name']  
    body = {'email': user_email, 'password': user_password}
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    resp = requests.post("https://practice.expandtesting.com/notes/api/users/login", headers=headers, data=body)
    respJS = resp.json()
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
    delete_user_api(randomData)
    delete_json_file(randomData)
    time.sleep(5)

def test_login_user_api_bad_request():
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_email = data['user_email']
    user_id = data['user_id']    
    user_password = data['user_password']  
    user_name = data['user_name']  
    body = {'email': '@'+user_email, 'password': user_password}
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    resp = requests.post("https://practice.expandtesting.com/notes/api/users/login", headers=headers, data=body)
    respJS = resp.json()
    assert False == respJS['success']
    assert 400 == respJS['status']
    assert "A valid email address is required" == respJS['message']
    login_user_api(randomData)
    delete_user_api(randomData)
    delete_json_file(randomData)
    time.sleep(5)

def test_login_user_api_unauthorized():
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_email = data['user_email']
    user_id = data['user_id']    
    user_password = data['user_password']  
    user_name = data['user_name']  
    body = {'email': user_email, 'password': '@'+user_password}
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    resp = requests.post("https://practice.expandtesting.com/notes/api/users/login", headers=headers, data=body)
    respJS = resp.json()
    assert False == respJS['success']
    assert 401 == respJS['status']
    assert "Incorrect email address or password" == respJS['message']
    login_user_api(randomData)
    delete_user_api(randomData)
    delete_json_file(randomData)
    time.sleep(5)

def test_get_user_api():
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
    login_user_api(randomData)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_email = data['user_email']
    user_id = data['user_id']     
    user_name = data['user_name'] 
    user_token = data['user_token'] 
    headers = {'accept': 'application/json', 'x-auth-token': user_token}
    resp = requests.get("https://practice.expandtesting.com/notes/api/users/profile", headers=headers)
    respJS = resp.json()
    assert True == respJS['success']
    assert 200 == respJS['status']
    assert "Profile successful" == respJS['message']
    assert user_email == respJS['data']['email']
    assert user_id == respJS['data']['id']
    assert user_name == respJS['data']['name']
    delete_user_api(randomData)
    delete_json_file(randomData)
    time.sleep(5)

def test_get_user_api_unauthorized():
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
    login_user_api(randomData)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_email = data['user_email']
    user_id = data['user_id']     
    user_name = data['user_name'] 
    user_token = data['user_token'] 
    headers = {'accept': 'application/json', 'x-auth-token': "@"+user_token}
    resp = requests.get("https://practice.expandtesting.com/notes/api/users/profile", headers=headers)
    respJS = resp.json()
    assert False == respJS['success']
    assert 401 == respJS['status']
    assert "Access token is not valid or has expired, you will need to login" == respJS['message']
    delete_user_api(randomData)
    delete_json_file(randomData)
    time.sleep(5)

def test_update_user_api():
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
    login_user_api(randomData)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_company = Faker().company()
    user_email = data['user_email']
    user_id = data['user_id']     
    user_name = Faker().name()
    user_phone = Faker().bothify(text='############')
    user_token = data['user_token'] 
    body = {'company': user_company, 'phone': user_phone, 'name': user_name}
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded', 'x-auth-token': user_token}
    resp = requests.patch("https://practice.expandtesting.com/notes/api/users/profile", headers=headers, data=body)
    respJS = resp.json()
    assert True == respJS['success']
    assert 200 == respJS['status']
    assert "Profile updated successful" == respJS['message']
    assert user_company == respJS['data']['company']
    assert user_email == respJS['data']['email']
    assert user_id == respJS['data']['id']
    assert user_name == respJS['data']['name']
    assert user_phone == respJS['data']['phone']
    delete_user_api(randomData)
    delete_json_file(randomData)
    time.sleep(5)

def test_update_user_api_bad_request():
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
    login_user_api(randomData)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_company = Faker().company()
    user_email = data['user_email']
    user_id = data['user_id']     
    user_name = Faker().name()
    user_phone = Faker().bothify(text='############')
    user_token = data['user_token'] 
    body = {'company': user_company, 'phone': user_phone, 'name': "a@#"}
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded', 'x-auth-token': user_token}
    resp = requests.patch("https://practice.expandtesting.com/notes/api/users/profile", headers=headers, data=body)
    respJS = resp.json()
    assert False == respJS['success']
    assert 400 == respJS['status']
    assert "User name must be between 4 and 30 characters" == respJS['message']
    delete_user_api(randomData)
    delete_json_file(randomData)
    time.sleep(5)

def test_update_user_api_unauthorized():
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
    login_user_api(randomData)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_company = Faker().company()
    user_email = data['user_email']
    user_id = data['user_id']     
    user_name = Faker().name()
    user_phone = Faker().bothify(text='############')
    user_token = data['user_token'] 
    body = {'company': user_company, 'phone': user_phone, 'name': user_name}
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded', 'x-auth-token': '@'+user_token}
    resp = requests.patch("https://practice.expandtesting.com/notes/api/users/profile", headers=headers, data=body)
    respJS = resp.json()
    assert False == respJS['success']
    assert 401 == respJS['status']
    assert "Access token is not valid or has expired, you will need to login" == respJS['message']
    delete_user_api(randomData)
    delete_json_file(randomData)
    time.sleep(5)

def test_update_user_password_api():
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
    login_user_api(randomData)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_password = data['user_password']
    user_new_password = Faker().password(length=12, special_chars=False, digits=True, upper_case=True, lower_case=True)
    user_token = data['user_token'] 
    body = {'currentPassword': user_password, 'newPassword': user_new_password}
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded', 'x-auth-token': user_token}
    resp = requests.post("https://practice.expandtesting.com/notes/api/users/change-password", headers=headers, data=body)
    respJS = resp.json()
    assert True == respJS['success']
    assert 200 == respJS['status']
    assert "The password was successfully updated" == respJS['message']
    delete_user_api(randomData)
    delete_json_file(randomData)
    time.sleep(5)

def test_update_user_password_api_bad_request():
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
    login_user_api(randomData)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_password = data['user_password']
    user_token = data['user_token'] 
    body = {'currentPassword': user_password, 'newPassword': "123"}
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded', 'x-auth-token': user_token}
    resp = requests.post("https://practice.expandtesting.com/notes/api/users/change-password", headers=headers, data=body)
    respJS = resp.json()
    assert False == respJS['success']
    assert 400 == respJS['status']
    assert "New password must be between 6 and 30 characters" == respJS['message']
    delete_user_api(randomData)
    delete_json_file(randomData)
    time.sleep(5)

def test_update_user_password_api_unauthorized():
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
    login_user_api(randomData)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_password = data['user_password']
    user_new_password = Faker().password(length=12, special_chars=False, digits=True, upper_case=True, lower_case=True)
    user_token = data['user_token'] 
    body = {'currentPassword': user_password, 'newPassword': user_new_password}
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded', 'x-auth-token': "@"+user_token}
    resp = requests.post("https://practice.expandtesting.com/notes/api/users/change-password", headers=headers, data=body)
    respJS = resp.json()
    assert False == respJS['success']
    assert 401 == respJS['status']
    assert "Access token is not valid or has expired, you will need to login" == respJS['message']
    delete_user_api(randomData)
    delete_json_file(randomData)
    time.sleep(5)

def test_logout_user_api():
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
    login_user_api(randomData)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_token = data['user_token']
    headers = {'accept': 'application/json', 'x-auth-token': user_token}
    resp = requests.delete("https://practice.expandtesting.com/notes/api/users/logout", headers=headers)
    respJS = resp.json()
    assert True == respJS['success']
    assert 200 == respJS['status']
    assert "User has been successfully logged out" == respJS['message']
    login_user_api(randomData)
    delete_user_api(randomData)
    delete_json_file(randomData)
    time.sleep(5)

def test_logout_user_api_unauthorized():
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
    login_user_api(randomData)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_token = data['user_token']
    headers = {'accept': 'application/json', 'x-auth-token': '@'+user_token}
    resp = requests.delete("https://practice.expandtesting.com/notes/api/users/logout", headers=headers)
    respJS = resp.json()
    assert False == respJS['success']
    assert 401 == respJS['status']
    assert "Access token is not valid or has expired, you will need to login" == respJS['message']
    login_user_api(randomData)
    delete_user_api(randomData)
    delete_json_file(randomData)
    time.sleep(5)

def test_delete_user_api():
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
    login_user_api(randomData)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_token = data['user_token']
    headers = {'accept': 'application/json', 'x-auth-token': user_token}
    resp = requests.delete("https://practice.expandtesting.com/notes/api/users/delete-account", headers=headers)
    respJS = resp.json()
    assert True == respJS['success']
    assert 200 == respJS['status']
    assert "Account successfully deleted" == respJS['message']
    delete_json_file(randomData)
    time.sleep(5)

def test_delete_user_api_unauthorized():
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_api(randomData)
    login_user_api(randomData)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_token = data['user_token']
    headers = {'accept': 'application/json', 'x-auth-token': '@'+user_token}
    resp = requests.delete("https://practice.expandtesting.com/notes/api/users/delete-account", headers=headers)
    respJS = resp.json()
    assert False == respJS['success']
    assert 401 == respJS['status']
    assert "Access token is not valid or has expired, you will need to login" == respJS['message']
    delete_json_file(randomData)
    time.sleep(5)

def create_user_api(randomData):
    user_email = Faker().company_email().replace("-", "")
    user_name = Faker().name()
    user_password = Faker().password(length=12, special_chars=False, digits=True, upper_case=True, lower_case=True)
    body = {'confirmPassword': user_password, 'email': user_email, 'name': user_name, 'password': user_password}
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    resp = requests.post("https://practice.expandtesting.com/notes/api/users/register", headers=headers, data=body)
    respJS = resp.json()
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

def login_user_api(randomData):
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_email = data['user_email']
    user_id = data['user_id']    
    user_password = data['user_password']  
    user_name = data['user_name']  
    body = {'email': user_email, 'password': user_password}
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    resp = requests.post("https://practice.expandtesting.com/notes/api/users/login", headers=headers, data=body)
    respJS = resp.json()
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
    
def delete_user_api(randomData):
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_token = data['user_token']
    headers = {'accept': 'application/json', 'x-auth-token': user_token}
    resp = requests.delete("https://practice.expandtesting.com/notes/api/users/delete-account", headers=headers)
    respJS = resp.json()
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
    assert True == respJS['success']
    assert 200 == respJS['status']
    assert "Note successfully deleted" == respJS['message']

def delete_json_file(randomData):
    os.remove(f"./tests/fixtures/file-{randomData}.json")


