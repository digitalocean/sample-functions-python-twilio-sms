import os
from http import HTTPStatus

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client


def translate_code(code):
    '''
    Takes in the twilio status code,
    returns a http status code.

        Parameters:
            args: Contains the twilio error status code

        Returns:
            json statusCode: Json http error status code
    '''

    supported_codes = {
        60000: HTTPStatus.BAD_REQUEST,
        60001: HTTPStatus.UNAUTHORIZED,
        60002: HTTPStatus.BAD_REQUEST,
        60003: HTTPStatus.TOO_MANY_REQUESTS,
        60004: HTTPStatus.BAD_REQUEST,
        60005: HTTPStatus.BAD_REQUEST,
        60021: HTTPStatus.FORBIDDEN,
        60022: HTTPStatus.UNAUTHORIZED,
        60023: HTTPStatus.NOT_FOUND,
        60033: HTTPStatus.BAD_REQUEST,
        60042: HTTPStatus.BAD_REQUEST,
        60046: HTTPStatus.BAD_REQUEST,
        60060: HTTPStatus.SERVICE_UNAVAILABLE,
        60064: HTTPStatus.FORBIDDEN,
        60065: HTTPStatus.FORBIDDEN,
        60066: HTTPStatus.FORBIDDEN,
        60069: HTTPStatus.BAD_REQUEST,
        60070: HTTPStatus.BAD_REQUEST,
        60071: HTTPStatus.NOT_FOUND,
        60072: HTTPStatus.NOT_FOUND,
        60073: HTTPStatus.BAD_REQUEST,
        60074: HTTPStatus.BAD_REQUEST,
        60075: HTTPStatus.BAD_REQUEST,
        60078: HTTPStatus.FORBIDDEN,
        60082: HTTPStatus.FORBIDDEN,
        60083: HTTPStatus.FORBIDDEN
    }

    if code in supported_codes:
        return supported_codes[code]

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
        client.lookups.phone_numbers(number).fetch(type="carrier")
        return True
    except TwilioRestException as e:
        return False


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
            "statusCode": HTTPStatus.BAD_REQUEST,
            "body": "no number provided"
        }
    if not user_to:
        return {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "body": "no receiver phone number provided"
        }
    if not message:
        return {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "body": "no message provided"
        }

    client = Client(sid, token)
    if valid_number(number, client) and valid_number(user_to, client):
        msg = client.messages.create(
            body=message,
            from_=number,
            to=user_to
        )
        if msg.status != "undelivered" or msg.status != "failed":
            return {
                "statusCode": HTTPStatus.ACCEPTED,
                "body": "success"
            }
        code = translate_code(msg.error_code)
        return {
            "statusCode": code,
            "body": msg.error_message
        }
    return {
        "statusCode": HTTPStatus.BAD_REQUEST,
        "body": "no twilio verified phone numbers provided"
    }
