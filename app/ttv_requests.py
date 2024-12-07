import requests
import os
from dotenv import load_dotenv; load_dotenv()


class TTV_requests():
    def __init__(self):
        self.base_url = 'https://api.twitch.tv/helix'
        self.client_id = str(os.getenv('CLIENT_ID'))
        self.client_secret = str(os.getenv('CLIENT_SECRET'))
        self.broadcaster_name = str(os.getenv('BROADCASTER_NAME')).lower()
        self.access_token = str(os.getenv('BROADCASTER_ACCESS_TOKEN'))
        self.broadcaster_id = str(self.fetch_user_id(self.broadcaster_name))


    def fetch_user_id(self, username: str):
        url = f'{self.base_url}/users'
        
        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.access_token}'
        }

        params = {
            'login': username
        }

        response = requests.get(url=url, headers=headers, params=params)
        response_data = response.json()

        user_id = response_data['data'][0]['id']

        return user_id
    

    def is_live(self):
        url = f'{self.base_url}/streams'

        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.access_token}'
        }

        response = requests.get(url=url, headers=headers)
        response_data = response.json()

        if response_data['data']:
            return True
        
        else:
            return False


    def get_chatters(self):

        chatters_list = []

        url = f'{self.base_url}/chat/chatters?broadcaster_id={self.broadcaster_id}&moderator_id={self.broadcaster_id}'

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Client-Id': self.client_id,
        }

        response = requests.get(url=url, headers=headers)

        response_data = response.json()

        for chatter in response_data['data']:
            chatter_name = str(chatter['user_name']).lower()
            chatters_list.append(chatter_name)

        return chatters_list
    

    def get_moderators(self):

        moderator_list = []

        url = f'{self.base_url}/moderation/moderators?broadcaster_id={self.broadcaster_id}'

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Client-Id': self.client_id,
        }

        params = {
            'first': 100
        }

        response = requests.get(url=url, headers=headers, params=params)

        response_data = response.json()

        for moderator in response_data['data']:
            moderator_name = str(moderator['user_name']).lower()
            moderator_list.append(moderator_name)

        moderator_list.append(self.broadcaster_name)

        return moderator_list
    

    def get_followers(self):
        follower_list = []

        url = f'{self.base_url}/channels/followers?broadcaster_id={self.broadcaster_id}'
    
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Client-Id': self.client_id,
        }

        params = {
            'first': 100
        }

        response = requests.get(url=url, headers=headers, params=params)
        response_data = response.json()

        for follower in response_data['data']:
            follower_name = str(follower['user_name']).lower()

            follower_list.append(follower_name)

        return follower_list
    

    def get_vips(self):
        vips_list = []

        url = f'{self.base_url}/channels/vips?broadcaster_id={self.broadcaster_id}'
    
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Client-Id': self.client_id,
        }

        params = {
            'first': 100
        }

        response = requests.get(url=url, headers=headers, params=params)
        response_data = response.json()

        for vip in response_data['data']:
            vip_name = str(vip['user_name']).lower()
            vips_list.append(vip_name)

        return vips_list


    def is_moderator(self, username):
        moderator_list = self.get_moderators()

        if username in moderator_list:
            return True
        
        else:
            return False
        
    
    def get_games(self, game_name: str):
        url = f'{self.base_url}/games?name={game_name}'

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Client-Id': self.client_id,
        }
        
        response = requests.get(url =url, headers=headers)
        
        response_data = response.json()

        if response.status_code == 200:
            game_id = response_data['data'][0]['id']

            return game_id

        else:
            return False
        

    # Types title, game
    def modify_channel_information(self, type: str, data):
        url = f'{self.base_url}/channels?broadcaster_id={self.broadcaster_id}'

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Client-Id': self.client_id,
            'Content-Type': 'application/json'
        }

        if type == 'title':
            params = {
                'title': str(data)
            }

        elif type == 'game':
            game_id = self.get_games(data)

            if not game_id:
                return False
            
            else:
                params = {
                'game_id': str(game_id)
                }

        response = requests.patch(url=url, headers=headers, params=params)

        print(f'[Info] Status code in modify_channel_information: {response.status_code}')

        if response.status_code == 204:
            return True
        
        else:
            return False