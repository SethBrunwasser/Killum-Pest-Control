from flask import Flask, render_template

app = Flask(__name__)

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

@app.route("/submitted")
def submitted():
    return render_template("submitted.html")
    # Code to contact owner

@app.route("/validation", methods=['GET', 'POST'])
def validation():
    # Form validation
    pass

    return render_template("submitted")

if __name__ == '__main__':
    app.run(debug=True)
