#!/usr/bin/env python3

# Libraries
import requests, sys

# Constants
TR_URL = 'https://translate.argosopentech.com/translate'
TR_HEADERS = {"Content-Type": "application/json"}

# Functions
def translate(text: str) -> str:
    """Return Italian translation of English text"""
    body = {
        'q':        text,
        'source':   'en',
        'target':   'it',
        'format':   'text'
    }
    
    request = requests.post(TR_URL, headers=TR_HEADERS, json=body)
    response = request.json()
    return response['translatedText']

if __name__ == '__main__':
    for line in sys.stdin:
        print(f'{translate(line.strip())}')
