import os
import json
import asyncio
from ttv_requests import TTV_requests

# Loyalty class
class Loyalty():
    def __init__(self):
        self.filename = f'json/loyalty.json'
        self.follower_list = []
        self.chatters_list = []
        self.loyalty_dict = self.load_loyalty_dict()
        self.ttv_requests = TTV_requests()
        self.was_live = self.ttv_requests.is_live()


    def load_loyalty_dict(self):
        try:
            with open(f'{self.filename}', 'r') as load_file:
                return json.load(load_file)

        except:
            return {}


    def save_loyalty_dict(self):
        if not os.path.exists('json'):
                os.makedirs('json')

        with open(f'{self.filename}', 'w') as save_file:
            json.dump(self.loyalty_dict, save_file, indent=4)


    async def loyalty_loop(self):
        while True:
            if self.ttv_requests.is_live():
                self.was_live = True
                self.follower_list = self.ttv_requests.get_followers()
                self.chatters_list = self.ttv_requests.get_chatters()

                self.load_loyalty_dict()

                for user in self.chatters_list:
                    if user in self.follower_list:
                        if user not in self.loyalty_dict:
                            self.loyalty_dict[f'{user}'] = 0

                        else:
                            self.loyalty_dict[f'{user}'] += 10
                    
            else:
                if self.was_live:
                    self.save_loyalty_dict()

                    self.was_live = False

            await asyncio.sleep(10)

            self.save_loyalty_dict()


    def get_user_loyalty(self, username):
        try:
            user_loyalty = self.loyalty_dict[f'{username}']

        except:
            user_loyalty = 0

        return user_loyalty





async def async_setup():
    loyalty = Loyalty()
    await loyalty.loyalty_loop()

def setup():
    asyncio.run(async_setup())

if __name__ == '__main__':
    setup()