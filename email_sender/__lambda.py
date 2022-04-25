import json

import urllib3

http = urllib3.PoolManager()


def lambda_handler(event, context):
    message_text = "New posts!\n"

    for idx, message in enumerate(event["Records"], 1):
        url = message["messageAttributes"]["url"]["stringValue"]
        message_text += f'<a href="{url}">{idx}. Watch on the website</a>'

    http.request(
        "GET",
        "http://api.telegram.org/bot<TOKEN>/sendMessage",
        fields={"chat_id": 630665299, "text": message_text, "parse_mode": "html"},
    )

    return {"statusCode": 200, "body": json.dumps("Hello from Lambda!")}
