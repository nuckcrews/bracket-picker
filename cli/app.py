import os
from openai import OpenAI
from .utils import announce, prompt_string, num_tokens
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

    total_tokens = 0
    def token_callback(text):
        nonlocal total_tokens
        total_tokens += num_tokens(text)

    bracket = Bracket(client, prompt, token_callback)

    def callback(round, winners):
        print("\nRound", round)
        announce(winners)

    bracket.generate_bracket(callback)

    print("Total Tokens:", total_tokens)
    announce("Bracket Picker is done!")