import requests
import json

API_URL = 'https://api.vk.com/method/'


def vk_api_request(method, token, params):
    params['access_token'] = token
    params['v'] = '5.131'  # Версия API
    response = requests.get(API_URL + method, params=params)
    return response.json()


def get_friends(token, user_id):
    friends_response = vk_api_request('friends.get', token, {'user_id': user_id})
    friends = friends_response.get('response', {}).get('items', [])
    friends_data = {}

    for friend_id in friends:
        try:
            friend_friends_response = vk_api_request('friends.get', token, {'user_id': friend_id})
            friend_friends = friend_friends_response.get('response', {}).get('items', [])
            friends_data[friend_id] = friend_friends
        except Exception as e:
            print(f"Error fetching friends of {friend_id}: {e}")
            continue

    keys_to_delete = [key for key, value in friends_data.items() if len(value) <= 0]
    
    for key in keys_to_delete:
        del friends_data[key]

    return friends_data


def save_to_json(data, filename='friends_data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
