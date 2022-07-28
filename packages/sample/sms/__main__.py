from http import HTTPStatus
import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

def translateCode(code):
    '''
    Takes in the twilio status code, 
    returns a http status code.

        Parameters:
            args: Contains the twilio error status code

        Returns:
            json statusCode: Json http error status code
    '''
    if str(code) == "60000":
        return HTTPStatus.BAD_REQUEST
    elif str(code) == "60001":
        return HTTPStatus.UNAUTHORIZED
    elif str(code) == "60002":
        return HTTPStatus.BAD_REQUEST
    elif str(code) == "60003":
        return HTTPStatus.TOO_MANY_REQUESTS
    elif str(code) == "60004":
        return HTTPStatus.BAD_REQUEST
    elif str(code) == "60005":
        return HTTPStatus.BAD_REQUEST
    elif str(code) == "60021":
        return HTTPStatus.FORBIDDEN
    elif str(code) == "60022":
        return HTTPStatus.UNAUTHORIZED
    elif str(code) == "60023":
        return HTTPStatus.NOT_FOUND
    elif str(code) == "60033":
        return HTTPStatus.BAD_REQUEST
    elif str(code) == "60042":
        return HTTPStatus.BAD_REQUEST
    elif str(code) == "60046":
        return HTTPStatus.BAD_REQUEST
    elif str(code) == "60060":
        return HTTPStatus.SERVICE_UNAVAILABLE
    elif str(code) == "60064":
        return HTTPStatus.FORBIDDEN
    elif str(code) == "60065":
        return HTTPStatus.FORBIDDEN
    elif str(code) == "60066":
        return HTTPStatus.FORBIDDEN
    elif str(code) == "60069":
        return HTTPStatus.BAD_REQUEST
    elif str(code) == "60070":
        return HTTPStatus.BAD_REQUEST
    elif str(code) == "60071":
        return HTTPStatus.NOT_FOUND
    elif str(code) == "60072":
        return HTTPStatus.NOT_FOUND
    elif str(code) == "60073":
        return HTTPStatus.BAD_REQUEST
    elif str(code) == "60074":
        return HTTPStatus.BAD_REQUEST
    elif str(code) == "60075":
        return HTTPStatus.BAD_REQUEST
    elif str(code) == "60078":
        return HTTPStatus.FORBIDDEN
    elif str(code) == "60082":
        return HTTPStatus.FORBIDDEN
    elif str(code) == "60083":
        return HTTPStatus.FORBIDDEN
    else:
        return HTTPStatus.INTERNAL_SERVER_ERROR

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
    message = args.get("message")

    if not number:
        return {
        "statusCode" : HTTPStatus.BAD_REQUEST,
        "body" : "no number provided"
    }
    if not user_to:
        return {
        "statusCode" : HTTPStatus.BAD_REQUEST,
        "body" : "no receiver phone number provided"
    }
    if not message:
        return {
        "statusCode" : HTTPStatus.BAD_REQUEST,
        "body" : "no message provided"
    }

    client = Client(sid, token)
    if valid_number(number, client) and valid_number(user_to, client):
        msg = client.messages.create(
            body = message,
            from_ = number,
            to = user_to
        )
        if msg.error_code == "null" or msg.error_code == "":
            return {
                "statusCode" : HTTPStatus.ACCEPTED,
                "body" : "success"
            }    
        code = translateCode(msg.error_code)
        return {
            "statusCode" : code,
            "body" : msg.error_message
        }         
    return {
        "statusCode" : HTTPStatus.BAD_REQUEST,
        "body" : "no twilio verified phone numbers provided"
    }