import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

def valid_number(number, client):
    try: 
        client.lookups.phone_numbers(number).fetch(type = "carrier")
        return True
    except TwilioRestException as e:
        if e == 21606:
            return False
        else:
            raise e


def main(args):
    sid = os.getenv('TWILIO_ACCOUNT_SID')
    token = os.getenv('TWILIO_AUTH_TOKEN')
    number = args.get("from")
    user_to = args.get("number")
    message = args.get("message", "this was sent from a twilio sms number")

    if not number:
        return {"body" : "no number provided"}
    if not user_to:
        return {"body" : "no receiver phone number provided"}
    if not message:
        return {"body" : "no message provided"}

    client = Client(sid, token)
    if (valid_number(number, client) == True) & (valid_number(user_to, client) == True):
        client.messages.create(
            body = message,
            from_ = number,
            to = user_to
        )
        return {"body" : "message sent"}
    else:
        return {"body" : "phone numbers provided are not twilio verified numbers"}

