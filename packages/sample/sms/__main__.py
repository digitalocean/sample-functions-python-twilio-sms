import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

def valid_number(number, client):
    '''
    Returns true if the number given is a valid twilio phone number.

        Parameters:
            number: Phone number provided to validate
            client: Connects to Twilio API

        Returns:
            boolean: True if valid phone number, false if invalid phone number
    '''
    try: 
        client.lookups.phone_numbers(number).fetch(type = "carrier")
        return True
    except TwilioRestException as e:
        if e == 21606:
            return False
        else:
            raise e


def main(args):
    '''
    Takes in the phone numbers and message to send an sms using Twilio, 
    returns a json response letting the user know if the message sent or failed to send.

        Parameters:
            args: Contains the from phone number, to phone number, and message to send

        Returns:
            json body: Json response if the message sent successfully or if an error happened
    '''
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
    if valid_number(number, client) and valid_number(user_to, client):
        client.messages.create(
            body = message,
            from_ = number,
            to = user_to
        )
        return {"body" : "message sent"}
    else:
        return {"body" : "phone numbers provided are not twilio verified numbers"}

