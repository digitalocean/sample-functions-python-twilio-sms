# Sample Function: Python "Twilio SMS"

## Introduction

This repository contains a sample Twilio SMS function written in Python. You are able to send an sms using Twilio verified phone numbers. You can deploy it on DigitalOcean's App Platform as a Serverless Function component.
Documentation is available at https://docs.digitalocean.com/products/functions.

### Requirements

* You need a DigitalOcean account. If you don't already have one, you can sign up at [https://cloud.digitalocean.com/registrations/new](https://cloud.digitalocean.com/registrations/new).
* You need a Twilio account. If you don't already have one, you can sign up at https://www.twilio.com/try-twilio.
* To send and receive sms with Twilio, you need a Twilio virtual phone number. You can learn more at https://www.twilio.com/docs/phone-numbers.
* The phone number you are sending a message to also has to be a twilio verified phone number.
* You need to add your `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN` to the `.env` file to connect to the Twilio API.
* To deploy from the command line, you will need the [DigitalOcean `doctl` CLI](https://github.com/digitalocean/doctl/releases).


## Deploying the Function

```bash
# clone this repo
git clone git@github.com:digitalocean/sample-functions-python-twilio-sms.git
```

```
# deploy the project, using a remote build so that compiled executable matched runtime environment
> doctl serverless deploy sample-functions-python-twilio-sms --remote-build
Deploying 'sample-functions-python-twilio-sms'
  to namespace 'fn-...'
  on host 'https://faas-...'
Submitted action 'sms' for remote building and deployment in runtime python:default (id: ...)

Deployed functions ('doctl sls fn get <funcName> --url' for URL):
  - sample/sms
```

## Using the Function

```bash
doctl serverless functions invoke sample/sms -p from:1234567890 number:0123456789 message:Good Morning from Sammy.
```
```json
{
  "body": "message sent"
}
```

### To send an email using curl:
```
curl -X PUT -H 'Content-Type: application/json' {your-DO-app-url} -d '{"from":"1234567890", "number":"0123456789", "message":"Good Morning from Sammy."}' 
```

### Learn More

You can learn more about Functions and App Platform integration in [the official App Platform Documentation](https://www.digitalocean.com/docs/app-platform/).