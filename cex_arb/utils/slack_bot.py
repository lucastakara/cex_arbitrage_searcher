
from slack_sdk import WebClient


def post_message_to_slack(message, blocks=None):
    client = WebClient(token="xoxb-1309429882372-1587121352023-ws3mAslAf3mRkwKXDIELb5KK")
    channel_id = "C03QBTNG4AE"

    result = client.chat_postMessage(
        channel=channel_id,
        text=message
    )
    return result

