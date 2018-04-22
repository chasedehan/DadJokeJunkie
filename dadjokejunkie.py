import os
from flask import Flask, render_template, request
from send_jokes import sign_up
from flask_mysqldb import MySQL
from config import Defaults, DB

# Logging setup
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

# Template routing
_TEMPLATES_ = {
    "success": 'thanks.html',
    "stop": 'stop.html',
    "registered": 'registered.html',
    "bad": "bad.html"
}

# Database setup
app = Flask(__name__)
app.config['MYSQL_USER'] = DB.user
app.config['MYSQL_PASSWORD'] = DB.password
app.config['MYSQL_DB'] = DB.db
app.config['MYSQL_UNIX_SOCKET'] = os.path.join('/cloudsql', DB.unix_socket)

# Check if on the App engine
#if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
#    app.config['MYSQL_UNIX_SOCKET'] = os.path.join('/cloudsql', DB.unix_socket)
#else:
#    app.config['MYSQL_HOST'] = DB.host

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        logging.info("App start - os env: {}".format(os.getenv('SERVER_SOFTWARE', '')))
        logging.info("New signup, phone: {}".format(request.form['phone_number']))
        status = sign_up(request.form['phone_number'], mysql)
        logging.info("Signup status: {}".format(status))

        return render_template(_TEMPLATES_[status])

    # Get returns the index
    return render_template('index.html')


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    app.run(port=Defaults.port)
