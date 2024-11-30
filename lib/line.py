import os
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    PushMessageRequest,
)


class LineClient:
    def __init__(self):
        self.__access_token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
        self.configuration = Configuration(access_token=self.__access_token)

    def send_message(self, user_id: str, msg: str) -> None:
        with ApiClient(self.configuration) as api_client:
            line_bot_api = MessagingApi(api_client)

            message = {"to": user_id,
                       "messages": [
                           {'type': 'text',
                            'text': msg},
                       ]}
            push_message_request = PushMessageRequest.from_dict(message)
            line_bot_api.push_message(push_message_request)
