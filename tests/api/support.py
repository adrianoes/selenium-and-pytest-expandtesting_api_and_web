import json
import os
import requests
from faker import Faker

def create_user_api(randomData):
    user_email = Faker().company_email()
    user_name = Faker().name()
    user_password = Faker().password()
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
    with open(f"./tests/resources/file-{randomData}.json", 'w') as json_file:
        json.dump(combined_responses, json_file, indent=4)

def login_user_api(randomData):
    with open(f"./tests/resources/file-{randomData}.json", 'r') as json_file:
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
    with open(f"./tests/resources/file-{randomData}.json", 'w') as json_file:
        json.dump(combined_responses, json_file, indent=4)
    
def delete_user_api(randomData):
    with open(f"./tests/resources/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_token = data['user_token']
    headers = {'accept': 'application/json', 'x-auth-token': user_token}
    resp = requests.delete("https://practice.expandtesting.com/notes/api/users/delete-account", headers=headers)
    respJS = resp.json()
    assert True == respJS['success']
    assert 200 == respJS['status']
    assert "Account successfully deleted" == respJS['message']

def delete_json_file(randomData):
    os.remove(f"./tests/resources/file-{randomData}.json")