#!/usr/bin/env python3
from flask import Flask, request
import json

from modules.GroupMeBot import GroupMeBot
from modules.QuoteMachine import QuoteMachine
import modules.italian_free as italian

# Initialize bot
app = Flask(__name__)
with open("configuration.txt") as config_file:
    config = json.load(config_file)
jj2 = GroupMeBot(bot_id=config['bot_id'], group_id=config['group_id'],
                url=config['url'], admin=config['admin'], token=config['token'], 
                translate_enabled=bool(config['translate_enabled']))
qm = QuoteMachine("quotes.txt")

@app.route('/', methods=['POST'])
def receive() -> str:
    """Parse group messages and post appropriate responses"""
    # Receive group message
    response = request.json
    text = response['text']
    text_lower = "".join(c for c in text.lower() if c not in {',','.','?','!',':'})

    # Prevent self-reply
    if response['sender_type'] == 'bot':
        return 'ok', 200

    # Ignore normal messages
    if 'jj' not in text_lower.split():
        return 'ok', 200
    
    # Command - PING
    if 'ping' in text_lower:
        jj2.post(response['name'].split()[0] + ' pinged me!')

    # Command - WHO
    elif 'who' in text_lower:
        jj2.post(f'Definitely {jj2.random_person()}')
        
    # Command - TRANSLATE
    elif 'translate' in text_lower:
        if jj2.translate_enabled:
            jj2.post(f'{italian.translate(text_lower.split("translate")[1])}')
        else:
            jj2.post("Sorry, my translate feature is currently disabled")
    
    # Admin Commands
    elif response['name'] == jj2.admin:
        # Command - TOGGLE TRANSLATION
        if 'italian enable' in text_lower:
            jj2.translate_enabled = True
        elif 'italian disable' in text_lower:
            jj2.translate_enabled = False

        # Command - UPDATE QUOTES
        elif 'quotes update' in text_lower:
            qm.update_quotes()
        
        # Command - ADD QUOTE
        elif 'quotes add' in text_lower:
            new_quote = text.split('quotes add ')[1]
            qm.add_quote(new_quote)
            qm.update_quotes()
            jj2.post(f'"{new_quote}" added!')

        # Command - UPDATE MEMBERS
        elif 'members update' in text_lower:
            jj2.update_members()

        # Command - JJ QUOTE FOR ADMIN
        else:
            jj2.post(f'{qm.random_quote()}')
    
    # Command - JJ QUOTE
    else:
        jj2.post(f'{qm.random_quote()}')

    return 'ok', 200

def main():
    app.run(host='0.0.0.0', port=80)

if __name__ == '__main__':
    main()