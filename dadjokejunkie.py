from flask import Flask, render_template, request
from send_jokes import daily_fix, sign_up

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)
        # TODO: check phone number against the DB to see if it is already in use
        sign_up(request.form['phone_number'])
        return render_template('thanks.html')

    return render_template('index.html')


if __name__ == '__main__':
    # TODO: set process in here to automatically kick off at a particular time
    # Or this could be a separate application
    daily_fix()
    app.run(port=31000)
