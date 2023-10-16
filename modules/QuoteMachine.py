#!/usr/bin/env python3
import random

class QuoteMachine():
    """Create a machine for dolling out quotes"""
    def __init__(self, quotes_file_name: str):
        self.quotes_file_name = quotes_file_name
        self.quotes = None
        self.update_quotes()

    def update_quotes(self) -> None:
        """Load quote list from a file"""
        try:
            with open(self.quotes_file_name) as quotes_file:
                self.quotes = quotes_file.read().splitlines()
        except IOError:
            return
    
    def add_quote(self, quote: str) -> None:
        """Append a quote to the quotes file"""
        try:
            with open(self.quotes_file_name, "a") as quotes_file:
                print(quote, file=quotes_file)
        except IOError:
            return

    def random_quote(self) -> str:
        """Return a random quote"""
        if self.quotes is not None:
            return random.choice(self.quotes)
        else:
            return "Feed me more quotes"