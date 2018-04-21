from flask import Flask, render_template, request
from send_jokes import sign_up
from config import Defaults

# Logging setup
import logging
from time import strftime

logging.basicConfig(
    filename=strftime("dadjokes_%H_%M_%m_%d_%Y.log"),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p')

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        logging.info("New signup, phone: {}".format(request.form['phone_number']))
        status = sign_up(request.form['phone_number'])
        logging.info("Signup status: {}".format(status))
        if status == "success":
            return render_template('thanks.html')
        elif status == "stop":
            return render_template('stop.html')
        elif status == "registered":
            return render_template('registered.html')
        elif status == "bad":
            return render_template('bad.html')

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
