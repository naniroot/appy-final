import twilio.twiml
from twilio.rest import TwilioRestClient
import time

SERVER_NUMBER = "YOUR NUMBER"
SID = "YOUR SID"
TOKEN = "YOUR TOKEN"

 
def smsEcho():
    client = TwilioRestClient(SID,TOKEN)
    clientNumber = ""#request.args.get('From');
    clientTextContent = ""#request.args.get('Body').lower()
    client.sms.messages.create(to=clientNumber, from_=SERVER_NUMBER, body= clientTextContent)
    return "HelloWorld"
 
if __name__ == "__main__":
    print(smsEcho())

