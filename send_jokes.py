# send_jokes.py
from twilio.rest import Client

account_sid = "ACdd403c2cdf304cdfb3e00eae998b8a59"
auth_token = "39e9082f27f913a4d6107ce75187aeee"

client = Client(account_sid, auth_token)

def sign_up(phone_number):
    # TODO: check number against the DB to make sure it is ok
    # Then, send the first message to the customer
    message = """Welcome to DadJokeJunkie, we will get you started right now:
    
    What do you call a fake noodle? An Impasta!
                
    Reply with STOP at any time to opt out."""
    # TODO: need to validate the number first, to make sure it works. Twilio is 1 sec per number
    # Do I set up multiple phone numbers for higher throughput? Probably, but that adds a little cost
    try:
        client.api.account.messages.create(
            to=phone_number,
            from_="+18019358742",
            body=message)
        return True
    except:
        return False
    # TODO: write that phone number out to the DB

def daily_fix():
    # TODO: build out the daily process that will actually occur
    # Look up the users where Stop=0
    #
    # Then, look up the joke of the day - random number generator off length of the table
        # I'm thinking to pull down the entire list and randomly select for a given subset of users
        # So that people get different jokes - at least a different joke per phone number

    # Loop through each of the users, deliver their joke

    # Maybe multithread it according to the phone numbers so they run in parallel.


    # Need to generate webhook to make sure that when STOP, they flip the Stop flag in the DB
    return True

