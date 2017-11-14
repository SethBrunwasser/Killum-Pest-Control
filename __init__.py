import sqlite3
from flask import Flask, render_template, request
from contextlib import closing

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

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
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
