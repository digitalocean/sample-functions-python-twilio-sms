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
    match code:
        case "60000":
            return HTTPStatus.BAD_REQUEST
        case "60001":
            return HTTPStatus.UNAUTHORIZED
        case "60002":
            return HTTPStatus.BAD_REQUEST
        case "60003":
            return HTTPStatus.TOO_MANY_REQUESTS
        case "60004":
            return HTTPStatus.BAD_REQUEST
        case "60005":
            return HTTPStatus.BAD_REQUEST
        case "60021":
            return HTTPStatus.FORBIDDEN
        case "60022":
            return HTTPStatus.UNAUTHORIZED
        case "60023":
            return HTTPStatus.NOT_FOUND
        case "60032":
            return HTTPStatus.BAD_REQUEST
        case "60033":
            return HTTPStatus.BAD_REQUEST
        case "60042":
            return HTTPStatus.BAD_REQUEST
        case "60046":
            return HTTPStatus.BAD_REQUEST
        case "60060":
            return HTTPStatus.SERVICE_UNAVAILABLE
        case "60064":
            return HTTPStatus.FORBIDDEN
        case "60065":
            return HTTPStatus.FORBIDDEN
        case "60066":
            return HTTPStatus.FORBIDDEN
        case "60069":
            return HTTPStatus.BAD_REQUEST
        case "60070":
            return HTTPStatus.BAD_REQUEST
        case "60071":
            return HTTPStatus.NOT_FOUND
        case "60072":
            return HTTPStatus.NOT_FOUND
        case "60073":
            return HTTPStatus.BAD_REQUEST
        case "60074":
            return HTTPStatus.BAD_REQUEST
        case "60075":
            return HTTPStatus.BAD_REQUEST
        case "60078":
            return HTTPStatus.FORBIDDEN
        case "60082":
            return HTTPStatus.FORBIDDEN
        case "60083":
            return HTTPStatus.FORBIDDEN
        case _ :
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
    message = args.get("message", "this was sent from a twilio sms number")

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
        if msg.error_code == "null":
            return {
                "statusCode" : HTTPStatus.ACCEPTED,
                "body" : "success"
            }    
        code = translateCode(msg.error_code)
        return {
            "statusCode" : code,
            "body" : msg.error_code
        }         
    return {
        "statusCode" : HTTPStatus.BAD_REQUEST,
        "body" : "no twilio verified phone numbers provided"
    }