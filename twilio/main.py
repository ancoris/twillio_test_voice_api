#!/usr/bin/env python3

import time

from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse


ACCOUNT_SID = "<REPLACE_ME>"
AUTH_TOKEN = "<REPLACE_ME>"
DESTINATION_NUMBER = "<REPLACE_ME>"
SOURCE_NUMBER = "<REPLACE_ME>"


class TwilioClient:
    def __init__(self):
        account_sid = ACCOUNT_SID
        auth_token = AUTH_TOKEN
        self.client = Client(account_sid, auth_token)
        self.call_completed_successfully = False

    def main(self):
        self.list_calls()

        while not self.call_completed_successfully:
            self.make_call()

    def list_calls(self):
        call_list = self.client.calls.list()
        for call in call_list:
            print(
                f"call.status: {call.status}, call.duration: {call.duration}, call.to_formatted: {call.to_formatted}, call.answered_by: {call.answered_by}"
            )
            print("=================================================")

    def make_call(self):
        r = VoiceResponse()
        r.say(
            "A 100 metre wide pothole has opened up outside Buckingham Palace, city of Westminster, London, S W 1 A 1 A A . Your quest, should you choose to accept it, is to fill the hole and save the day.",
            voice="Google.en-GB-Standard-A",
            language="en-GB",
        )

        call = self.client.calls.create(
            from_=SOURCE_NUMBER,
            to=DESTINATION_NUMBER,
            twiml=str(r),
            machine_detection="Enable",
            machine_detection_timeout=6,
            async_amd=False,  # it blocks the call until the machine detection is complete which seems bad, but in the case that `answered_by` is `unknown` it will hang up and redial. if we set it to true, then if it is unknown then the message will have been part read and then gets hung up.
            # timeout=600,  # seems to cut out at 30 seconds on my trial account no matter what, however the docs say 600 is the max
        )

        print(call.sid, call.status)

        while call.status != "completed":
            time.sleep(1)
            call = self.client.calls(call.sid).fetch()
            print(call.status, call.answered_by)
            if call.answered_by:
                if call.answered_by == "human":
                    self.call_completed_successfully = True
                else:
                    self.hangup_call_inprogress(call.sid)

    def hangup_call_inprogress(self, sid):
        self.client.calls(sid).update(status="completed")


if __name__ == "__main__":
    TwilioClient().main()
