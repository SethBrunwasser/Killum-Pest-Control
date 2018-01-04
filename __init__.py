from __future__ import print_function
import sqlite3
from flask import Flask, render_template, request, current_app, g
from contextlib import closing
import httplib2
import os
import base64

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from email.mime.text import MIMEText

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'KillumPestControlTest'


def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'client_secret.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


# Configuration
DATABASE = '/tmp/init.db'
DEBUG = False
SECRET_KEY = 'z7zvPSta3PB3Hp2D'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
'''
def connect_db():
    rv = sqlite3.connect(current_app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
def init_db():
    with closing(connect_db()) as db:
        with current_app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
@app.before_request
def before_request():
    g.db = connect_db()
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
# Show Entries
@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries = entries)
# Add new entry
@app.route('/add', methods=['POST'])
def add_entry():
    g.db.execute('insert into entries (title, text) value (?, ?)',
                [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))
'''

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

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
        # Send Email to owner
        if validateForm(request.form['email'], request.form['subject'], request.form['name'], 
            request.form['phone'], request.form['message']):
            credentials = get_credentials()
            http = credentials.authorize(httplib2.Http())
            service = discovery.build('gmail', 'v1', http=http)

            new_msg = create_message('sbrunwasser1998@gmail.com', request.form['email'], 
                                        'Killum Pest Control - ' + request.form['subject'], 
                                        'From ' + request.form['name'] + 
                                        '\nPhone Number: ' + request.form['phone'] + '\n' +
                                         request.form['message'])
            sendEmail(service, 'me', new_msg)
        else:
            return render_template('contact.html')
    return render_template('submitted.html', error=error)

def validateForm(email, subject, name, phone, message):
    passingFlag = False
    if '@' not in email or email == '':
        return passingFlag
    elif subject == '':
        return passingFlag
    elif name == '':
        return passingFlag
    elif phone == '' or not phone.isdigit():
        return passingFlag
    elif subject == '':
        return passingFlag
    elif message == '':
        return passingFlag
    else:
        return True
def sendEmail(service, user_id, message):
    #try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    return message
    #except Exception as e:
    #    print(e)


def create_message(to, sender, subject, message_text):
  """Create a message for an email.
  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  raw = base64.urlsafe_b64encode(message.as_bytes())
  raw = raw.decode()
  return {'raw': raw}

if __name__ == '__main__':
    app.run(debug=True)