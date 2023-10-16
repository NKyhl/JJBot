#!/usr/bin/env python3
import requests
import random

class GroupMeBot():
    """Create a GroupMe Bot for sending messages"""
    def __init__(self, bot_id: str, group_id: str, url: str, admin: str,
                 token: str, translate_enabled: bool = False):
        self.bot_id            = bot_id
        self.group_id          = group_id
        self.url               = url
        self.admin             = admin
        self.token             = token
        self.translate_enabled = translate_enabled
        self.members           = None
        self.update_members()

    def post(self, msg: str) -> None:
        """Post message to GroupMe via HTTP request"""
        path    = '/v3/bots/post'
        data    = {"bot_id": self.bot_id, "text": msg}
        headers = {"Content-Type": "application/json"}
        requests.post(url=self.url+path, json=data, headers=headers)

    def random_person(self) -> str:
        """Return a random person from the group"""
        if self.members:
            return self.members[random.randint(0, len(self.members)-1)]
        else:
            return "Nobody"
    
    def update_members(self) -> list:
        """Update or set members attribute via HTTP request"""
        path           = f'/v3/groups/{self.group_id}'
        group_response = requests.get(f'{self.url+path}?token={self.token}').json()

        # Only change attribute if request is successful
        if group_response['meta']['code'] == 200:
            self.members = [person['name'] for person in group_response['response']['members']]