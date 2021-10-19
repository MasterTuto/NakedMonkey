from typing import Any, List, Tuple, Union

from credentials import API_KEY
from logger import pprint
from time import sleep
from codeforces import *
import requests
from random import choice, choices
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
    
    def get_commands(self, scope : Union[str, List[str]]):
        url = self.base_url.format(method="getMyCommands")

        scopes = [scope] if type(scope) == str else scope
        
        answers = []

        for scope in scopes:
            params = {"scope": {"type":  scope }}

            answers.append( requests.get(url, json=params) )
        return answers
    
    def set_commands(self, commands : list, scope: Union[str, List[str]]) -> bool:
        list_of_commands = [
            {"command": command_name, "description": description}
            for (command_name, description) in commands
        ]

        url = self.base_url.format( method="setMyCommands" )

        answers = []
        scopes = [scope] if type(scope) == str else scope
        for scope in scopes:
            data = { "commands": list_of_commands, "scope": { "type": scope  } }

            answers.append ( requests.post( url, json=data ) )

        return answers if len(answers) > 1 else answers[0]


    def delete_commands(self):
        url = self.base_url.format(method="deleteMyCommands")
        return requests.post( url )

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

    def parse_message(self, message: str) -> Tuple[List[str], Tuple[int, int], str, int]:
        rating : Tuple(int, int) = (-1, -1)
        tags : List[str] = []
        user = ""
        quantity = 1

        acc = ""
        for entry in message.split(" "):
            if len(entry.strip()) == 0: continue

            if entry.startswith("r:"): #rating
                entry = entry[2:]
                if entry.count("-") == 0 and entry.isnumeric():
                    rating = (int(entry), int(entry))
                elif entry.count('-') == 1:
                    (begin, end) = entry.split("-")
                    begin = int(begin) if begin.isnumeric() else -1
                    end = int(end) if end.isnumeric() else -1
                    
                    rating = (begin, end)
            elif entry.startswith("n:"):
                entry = entry[2:]
                if entry.isnumeric():
                    quantity = int(entry)
            elif entry.startswith("@"):
                user = entry[1:]
            elif entry.startswith('"'):
                acc += entry[1:] + " "
            elif entry.endswith('"'):
                acc += entry[:-1]
                tags.append( acc )
                acc = ""
            else:
                tags.append( entry )

        return tags, rating, user, ( quantity if quantity > 0 else 1 )

    
    def beautify_problem(self, problem: Problem) -> str:
        tags = ", ".join(problem.tags)
        # return f"{problem.contest_id}/{problem.index}: {problem.name}\nRating: {problem.rating}\nTags: {tags}\n{problem.url}\n"
        return f"{problem.contest_id}/{problem.index}: {problem.name}\nRating: {problem.rating}\n{problem.url}\n"
    
    def beautify_problems(self, problems: List[Problem]) -> str:
        if len(problems) == 0: return "Nenhum problema encontrado :/"

        result = f"{len(problems)}(s) problemas encontrados:\n\n"

        return result + "\n".join( [self.beautify_problem(p) for p in problems] )
    
    def send_random_problem(self, message):
        tags, rating, user, quantity = self.parse_message( message['text'][5:] )
        
        list_of_problems = self.cf.get_problems(*tags, begin_rating=rating[0], end_rating=rating[1], user=user)
        problems = choices( list_of_problems, k=min(quantity, len(list_of_problems)) )
        
        problem_txt = self.beautify_problems( problems )

        self.reply_to(message, problem_txt)

    def show_help(self, message):
        help_message = (
            "List of Commands:\n\n"
            "/help - this help message\n\n"
            "/rand - answers random codeforces question:\n"
            "        any word means a tag, multi word tags must be in quotation marks\n"
            "        r: specifies rating range ou exact rating\n"
            "        n: specifies the number of questions to answer\n"
            "        @ specifies what user to filter the questions they never submitted\n\n"
            "/recommend - almost like /rand, except that it uses user data to recommend "
            "a problem they should answer\n\n"
            "/gen - generates a pdf file for a contest, given the difficulty:\n"
            "        easy  = questions which rating *r* is ```800 <= r <= 1000 ```\n"
            "        medium  = questions which rating *r* is ```1000 < r <= 1800 ```\n"
            "        hard  = questions which rating *r* is ```1800 < r```\n"
        )

        self.reply_to(message, help_message)

    def send_recommendation(self, message):
        return self.reply_to(message, "vai pedir recomendacao sua mãe")
        

    def work(self, update: dict) -> None:
        commands = {
            "rand": lambda message: self.send_random_problem(message),
            "recommend": lambda message: self.send_recommendation(message),
            "help": lambda message: self.show_help(message)
        }

        if self.typeof(update) == 'message':
            if self.is_command( update ):
                command = update['message']['text'].split(" ", 1)[0][1:].split("@", 1)[0]
                
                if command in commands:
                    commands[command]( update['message'] )
                    
    def run(self):
        last_update : int = 0
        while True:
            updates = self.get_updates(offset=last_update+1).json()['result']

            for update in updates:
                self.work(update)
                last_update = update['update_id']

def main():
    bot = Telegram()

    bot.run()

if __name__ == "__main__":
    main()