import os
import json
from openai import OpenAI
import boto3 as boto
from src import Bracket, post_bracket

REQUEST_HANDLED = {"statusCode": 200}


def execute(event, context):
    if event["requestContext"]["eventType"] == "CONNECT":
        return REQUEST_HANDLED
    elif event["requestContext"]["eventType"] == "DISCONNECT":
        return REQUEST_HANDLED
    elif event["requestContext"]["eventType"] != "MESSAGE":
        raise ValueError("Invalid event type")

    client = OpenAI()
    client_key = os.getenv("OPENAI_API_KEY")
    if client_key:
        client.api_key = client_key
    else:
        raise ValueError("OPENAI_API_KEY is not set")

    body = json.loads(event["body"])
    prompt = body["prompt"]
    connection_id = event["requestContext"]["connectionId"]
    bracket = Bracket(client, prompt)

    full_bracket = []
    def callback(round, tournament):
        send_ws_message(connection_id, json.dumps({
            "round": round,
            "tournament": tournament
        }))
        nonlocal full_bracket
        full_bracket = tournament

    try:
        bracket.generate_bracket(callback)

        id = post_bracket(prompt, full_bracket)
    except Exception as e:
        send_ws_message(connection_id, json.dumps({
            "error": str(e)
        }))
        return REQUEST_HANDLED

    send_ws_message(connection_id, json.dumps({
        "bracket_id": id
    }))

    print("Bracket Picker is done!")
    return REQUEST_HANDLED

endpoint = os.environ["WEBSOCKET_API_ENDPOINT"]
api = boto.client("apigatewaymanagementapi", endpoint_url=endpoint)

def send_ws_message(connection_id, data):
    return api.post_to_connection(ConnectionId=connection_id, Data=data.encode("utf-8"))
