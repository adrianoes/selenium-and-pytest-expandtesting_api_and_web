import requests
s = requests.Session()

def test_sr():

    headers = {'x-auth-token': '19afc9fb132044969472b144d30baf2175ad97a8b60a494ab8c0dad9d44f736f', 'accept': 'application/json'}
    r = s.get("https://practice.expandtesting.com/notes/api/users/profile", headers=headers)
    print(r.json())
    response_json = r.json()
    user_id = response_json.get('data', {}).get('id', {})
    user_id2 = response_json['data']['id']
    # user_id2_when_there_is_index = response_json['data'][1]['id']
    print(user_id)
    print(user_id2)