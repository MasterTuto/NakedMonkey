import json

def logMessage(update : dict):
    message = getMessage(update)
    chat_id =  getChatId(update)

    print(f"[!] {chat_id} - New message: \"{message}\"")

def pprint(update: dict):
    print( json.dumps(update, indent=2) )