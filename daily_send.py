"""
This script sends out the daily messages for DadJokeJunkie.com

Will be kicked off by cron job, so all code in script will execute.

Steps:
1) Load all libraries and initialize everything
2) Select phone numbers from DB of people who are eligible (where Stop=0)
3) Randomly load joke of the day (from Jokes)
4) Write back to Jokes, incrementing the joke count
5) Update the DailyJokes (history table) with the joke of the day
6) Loop through user list, sending the joke to each user
7) If code returns "STOP" (or whatever it is), update Users table with Stop=1
8) Done

"""

# Step 1) Load all libraries and initialize everything
from twilio.rest import Client
import MySQLdb
import random
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

# Step 2) Select phone numbers from DB of people who are eligible (where Stop=0)
crsr = db.cursor()
crsr.execute("""select PhoneNumber from Users WHERE Stop = 0""")
phone_numbers = [x[0] for x in crsr.fetchall()]
crsr.close()


# Step 3) Randomly load joke of the day (from Jokes)
crsr = db.cursor()
crsr.execute("""select COUNT(*) from Jokes""")

joke_id = random.randint(1, crsr.fetchall()[0][0])
crsr.execute("""select JokeText from Jokes where JokeId = %s""", (joke_id, ))
todays_joke = crsr.fetchall()[0][0]
crsr.close()


# Step 4) Write back to Jokes, incrementing the joke count
crsr = db.cursor()
crsr.execute("""UPDATE Jokes SET TimesSent = TimesSent + 1 WHERE JokeId = %s""", (joke_id, ))
crsr.close()


# Step 5) Update the DailyJokes (history table) with the joke of the day
# Do this later


# Step 6) Loop through user list, sending the joke to each user
for phone_number in phone_numbers:
    try:
        client.api.account.messages.create(
            to=phone_number,
            from_=SMS.phone_one,
            body=todays_joke)
    except:
        pass
        # Do some stuff here, this would be on a STOP?


# Step 7) If code returns "STOP" (or whatever it is), update Users table with Stop=1


# Step 8) Done!



