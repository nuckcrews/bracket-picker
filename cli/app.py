import os
from openai import OpenAI
from .utils import announce, prompt_string
from src import Bracket

def main():
    os.system("clear")

    client = OpenAI()
    client_key = os.getenv("OPENAI_API_KEY")
    if client_key:
        client.api_key = client_key
    else:
        raise ValueError("OPENAI_API_KEY is not set")

    announce("Welcome to Bracket Picker")

    prompt = prompt_string("How should we pick your bracket?")

    bracket = Bracket(client, prompt)

    def callback(round, winners):
        print("\nRound", round)
        announce(winners)

    bracket.generate_bracket(callback)

    announce("Bracket Picker is done!")