# send_jokes.py
# TODO: create some logs so I can see what is happening
from twilio.rest import Client
from datetime import datetime
import MySQLdb
from config import SMS, DB

account_sid = SMS.account_sid
auth_token = SMS.auth_token

client = Client(account_sid, auth_token)
db = MySQLdb.connect(host=DB.host,
                     port=DB.port,
                     user=DB.user,
                     passwd=DB.password,
                     db=DB.db)
db.autocommit(True)


def sign_up(phone_number):
    crsr = db.cursor()
    exists = crsr.execute("""select Stop from Users WHERE PhoneNumber = %s LIMIT 1""", (phone_number,))
    crsr.close()
    if exists:
        crsr = db.cursor()
        crsr.execute("""select Stop from Users WHERE PhoneNumber = %s""", (phone_number,))
        stop = crsr.fetchall()[0][0]
        crsr.close()
        if stop:
            return "stop"
        return "registered"

    # Then, send the first message to the customer
    message = """Welcome to DadJokeJunkie, we will get you started right now:
    
    What do you call a fake noodle? An Impasta!
                
    Reply with STOP at any time to opt out."""

    try:
        client.api.account.messages.create(
            to=phone_number,
            from_=SMS.phone_one,
            body=message)
    except:
        return "bad"

    crsr = db.cursor()
    crsr.execute("""INSERT INTO Users
                  (PhoneNumber, Stop, CreatedDate)
                  VALUES (%s, 0, %s);""",
                 (phone_number, str(datetime.now())))
    crsr.close()
    return "success"

