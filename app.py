import os
import json
from openai import OpenAI
import boto3 as boto
from src import Bracket

REQUEST_HANDLED = {"statusCode": 200}


def execute(event, context):
    print(event)
    print(context)
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

    def callback(round, winners):
        print("\nRound", round)
        print(winners)
        send_ws_message(connection_id, json.dumps({
            "round": round,
            "winners": winners
        }))

    bracket.generate_bracket(callback)

    send_ws_message(connection_id, "DONE")

    print("Bracket Picker is done!")
    return REQUEST_HANDLED

endpoint = os.environ["WEBSOCKET_API_ENDPOINT"]
api = boto.client("apigatewaymanagementapi", endpoint_url=endpoint)

def send_ws_message(connection_id, data):
    return api.post_to_connection(ConnectionId=connection_id, Data=data.encode("utf-8"))
