from flask import Flask, render_template, request
from send_jokes import sign_up
from config import Defaults

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        status = sign_up(request.form['phone_number'])
        if status == "success":
            return render_template('thanks.html')
        elif status == "stop":
            return render_template('stop.html')
        elif status == "registered":
            return render_template('registered.html')
        elif status == "bad":
            return render_template('bad.html')

    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=Defaults.port)
