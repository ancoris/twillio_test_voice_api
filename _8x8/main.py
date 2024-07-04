#!/usr/bin/env python3

import requests

SUBACCOUNT_ID = "<REPLACE_ME>"
BEARER_TOKEN = "<REPLACE_ME>"
DESTINATION_NUMBER = "<REPLACE_ME>"


class _8x8Client:
    def main(self):
        self.sms_message()
        self.voice_message()

    def sms_message(self):
        url = f"https://sms.8x8.uk/api/v1/subaccounts/{SUBACCOUNT_ID}/messages"

        payload = {
            "encoding": "AUTO",
            "track": None,
            "destination": DESTINATION_NUMBER,
            "country": "GB",
            "source": "Test",
            "text": "My Test SMS",
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {BEARER_TOKEN}",
        }

        response = requests.post(url, json=payload, headers=headers)

        print(response.text)

    def voice_message(self):
        url = f"https://voice.wavecell.com/api/v1/subaccounts/{SUBACCOUNT_ID}/calls"

        payload = {
            "callflow": [
                {
                    "params": {
                        "source": "private",
                        "destination": DESTINATION_NUMBER,
                        "text": "8x8 test message",
                        "language": "en-GB",
                        "voiceProfile": "en-GB-Emma",
                        "repetition": 1,
                        "speed": 1,
                    },
                    "action": "say",
                }
            ]
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {BEARER_TOKEN}",
        }

        response = requests.post(url, json=payload, headers=headers)

        print(response.text)


if __name__ == "__main__":
    _8x8Client().main()
