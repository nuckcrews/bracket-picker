from PyInquirer import prompt
import tiktoken

__all__ = ["prompt_confirm", "prompt_string", "prompt_list", "announce", "num_tokens"]


def announce(message, prefix: str = ""):
    # Function to print a colored message

    cyan = '\033[96m'
    default = '\033[0m'
    print("{0}{1}{2}{3}".format(prefix, cyan, message, default))

def prompt_confirm(question_message, default=True):
    # Function to prompt a confirmation question

    return prompt(
        {
            'type': 'confirm',
            'name': 'name',
            'message': question_message,
            'default': default
        }
    ).get('name')


def prompt_string(question_message, default=None):
    # Function to prompt a string input question

    return prompt(
        {
            'type': 'input',
            'name': 'name',
            'message': question_message,
            'default': default if default else ""
        }
    ).get('name')


def prompt_list(question_message, choices, default=None):
    # Function to prompt a list selection question
    return prompt(
        {
            'type': 'list',
            'name': 'name',
            'message': question_message,
            'choices': choices,
            'default': default
        }
    ).get('name')

encoding_4 = tiktoken.encoding_for_model("gpt-4")
encoding_3_5 = tiktoken.encoding_for_model("gpt-3.5-turbo")
encoding_embedding = tiktoken.encoding_for_model("text-embedding-ada-002")

def num_tokens(content: str, model="gpt-4"):
    if model == "gpt-3.5-turbo":
        encoding = encoding_3_5
    elif model == "text-embedding-3-small":
        encoding = encoding_embedding
    else:
        encoding = encoding_4

    return len(encoding.encode(content))