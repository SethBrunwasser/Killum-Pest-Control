import sqlite3
from flask import Flask, render_template, request

# Configuration
DATABASE = '/tmp/init.db'
DEBUG = True
SECRET_KEY = 'z7zvPSta3PB3Hp2D'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/testimonials")
def testimonials():
    return render_template("testimonials.html")

@app.route("/submitted", methods=['GET', 'POST'])
def submitted():
    error = None
    if request.method == 'POST':
        if validation(request.estimateform['name'], request.estimateform['email'],
                    request.estimateform['phone'], request.estimateform['subject'],
                    request.estimateform['message']):

            # Send Email to owner
            sendEmail(request.estimateform['name'], request.estimateform['email'],
                        request.estimateform['phone'], request.estimateform['subject'],
                        request.estimateform['message'])
        else:
            error = 'Form not valid'
    return render_template('submitted.html', error=error)


    return render_template("submitted.html")

def sendEmail(name, email, phone, subject, message):
    submission = False

if __name__ == '__main__':
    app.run(debug=True)
