from typing import Any, List

from credentials import API_KEY
from logger import pprint
from time import sleep
from codeforces import CodeForces
import requests
from random import choice
import json
import sys


class Telegram:
    def __init__(self):
        self.base_url = "https://api.telegram.org/bot"+API_KEY+"/{method}"
        self.cf = CodeForces()

    def get_me(self) -> requests.Response:
        url = self.base_url.format( method='getMe' )

        return requests.get( url )

    def get_updates(self, **parameters) -> requests.Response:
        url = self.base_url.format(method="getUpdates")

        return requests.get(url, json=parameters)

    def get_chat_id(self, update : dict) -> int:
        return update['message']['chat']['id']

    def get_message(self, update: dict) -> str:
        print(update['message'])
        return update['message']['text'] if 'text' in update['message'] else None

    def send_message(self, chat_id, message, **other_args) -> requests.Response:
        if message == None: return
        url = self.base_url.format( method="sendMessage" )
        
        content = {
            "chat_id": chat_id,
            "text": message,
            **other_args
        }

        return requests.post(url, data=content)
    
    def set_commands(self, commands : list) -> bool:
        list_of_commands = [
            {"command": command_name, "description": description}
            for (command_name, description) in commands
        ]

        url = self.base_url.format( method="setMyCommands" )

        return requests.post( url, json=list_of_commands )

    def typeof(self, update: dict) -> str:
        possibilities = ['message']
        for possibility in possibilities:
            if possibility in update:
                return possibility

        return ''

    def is_command(self, update: dict):
        if 'entities' not in update['message']:
            return False

        entities = update['message']['entities']
        return any( entity['type']=='bot_command' for entity in entities )
        
    def reply_to(self, who, message : str):
        self.send_message(reply_to_message=who, chat_id=who['chat']['id'], message=message)
    
    def send_random_problem(self, message):
        all_tags : List[str] = message['text'][5:].split()
        tags = filter(lambda i: not i.isnumeric() and len(i.strip()) > 0, all_tags )
        
        ratings = list(filter( lambda x: x.isnumeric(), all_tags ))
        rating = ratings[0] if len(ratings) > 0 else -1


        list_of_problems = self.cf.get_problems(*tags, rating=int(rating))
        
        problem = choice( list_of_problems ).url if len(list_of_problems) > 0 else "Nenhum problema encontrado :/"

        self.reply_to(message, problem)

    def work(self, update: dict) -> None:
        if self.typeof(update) == 'message':
            if self.is_command( update ):
                if update['message']['text'].startswith('/rand'):
                    self.send_random_problem(update['message'])
        
    def run(self):
        last_update : int = 0
        while True:
            updates = self.get_updates(offset=last_update+1).json()['result']

            for update in updates:
                self.work(update)
                last_update = update['update_id']


def main():
    bot = Telegram()
    # bot.set_commands([("rand", "Manda uma questao aleatoria")])
    bot.run()

if __name__ == "__main__":
    main()