import os
import shortuuid
import boto3 as boto

__all__ = ["post_bracket"]

dynamodb = boto.resource("dynamodb")
table = dynamodb.Table(os.getenv("BRACKET_TABLE"))

def post_bracket(prompt, bracket):
    """Post a bracket to the database."""
    bracket_id = shortuuid.uuid()
    item = {
        "bracket_id": bracket_id,
        "prompt": prompt,
        "bracket": bracket
    }

    table.put_item(Item=item)

    return bracket_id