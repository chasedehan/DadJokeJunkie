# send_jokes.py
# TODO: create some logs so I can see what is happening
from twilio.rest import Client
from datetime import datetime

import logging
from config import SMS

_JOKE_0_ = """Welcome to DadJokeJunkie, we will get you started right now:

What do you call a fake noodle? An Impasta!

Reply with STOP at any time to opt out."""

account_sid = SMS.account_sid
auth_token = SMS.auth_token

client = Client(account_sid, auth_token)


def bad_num(number):
    # Checks to make sure a valid US phone number
    try:
        number = client.lookups.phone_numbers(number).fetch()
        country_code = number.country_code
        if country_code == "US":
            logging.info("US country code")
            return False
        else:
            logging.info("Non-US country code: {}".format(country_code))
            return True
    except:
        return True


def sign_up(phone_number, mysql):
    conn = mysql.connection
    cur = conn.cursor()
    logging.info("querying user from DB")

    # TODO - Need a stored proc for this
    exists = cur.execute("""select Stop from Users WHERE PhoneNumber = %s LIMIT 1""", (phone_number,))

    if exists:
        logging.info("User already registered")
        return "registered"

    if bad_num(phone_number):
        return "bad"

    # Then, send the first message to the customer
    try:
        client.api.account.messages.create(
            to=phone_number,
            from_=SMS.phone_one,
            body=_JOKE_0_)
        logging.info("welcome joke text sent")
    except:
        return "bad"

    # TODO - Need a stored proc for this
    cur.execute("""INSERT INTO Users
                (PhoneNumber, Stop, CreatedDate)
                VALUES (%s, 0, %s);""",
                (phone_number, str(datetime.now())))
    logging.info("User saved to DB")

    cur.callproc('Save_SentText', (phone_number, 0))
    conn.commit()
    logging.info("Text saved to DB")

    return "success"
