import os
import math

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_mail import Mail, Message
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from functools import wraps
from apscheduler.schedulers.background import BackgroundScheduler

# Configure application
app = Flask(__name__)
# app.run(debug=True)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configuration for flask_mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'notifications.duck64843@gmail.com'
app.config['MAIL_PASSWORD'] = 'txll vfbr mblb hfqw'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_SUPPRESS_SEND'] = False

# Initialise Mail
mail = Mail(app)

# Initiatlise scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///contactus.db")


# Adapted from: https://cs50.harvard.edu/x/2024/weeks/9/, which decorate routes to require a login
def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

# Adapted from: https://cs50.harvard.edu/x/2024/weeks/9/, to ensure users get the most up to date content from the server
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Client submits enquiry form"""
    if request.method == "POST":
        # Flash error if any essential field is missing
        if not request.form.get("fullname"):
            flash('Full Name must be provided.')
            return redirect("/")
        if not request.form.get("phone"):
            flash('Phone Number must be provided.')
            return redirect("/")
        if not request.form.get("email"):
            flash('Email Address must be provided.')
            return redirect("/")
        if not request.form.get("postcode"):
            flash('Postcode must be provided.')
            return redirect("/")
        if not request.form.get("turnaround"):
            flash('\'When is the work required?\' must be provided.')
            return redirect("/")
        if not request.form.get("enquiry"):
            flash('\'How can we help?\' must be provided.')
            return redirect("/")
        # Add the row to the database
        fullname = request.form.get("fullname")
        phone = request.form.get("phone")
        email = request.form.get("email")
        postcode = request.form.get("postcode")
        turnaround = request.form.get("turnaround")
        enquiry = request.form.get("enquiry")
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M")
        add_enquiry = """
            INSERT INTO enquiries (urgency, postcode, message, name, email, phone, date, status, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, "Not Contacted", "1")
        """
        db.execute(add_enquiry, turnaround, postcode, enquiry, fullname, email, phone, current_time)
        # Flash 'Thank you' message to user following form completion
        flash('Thank you for your enquiry. We\'ll be in touch soon.')
        # Sent triggered email to staff following form completion
        # Adapted from: https://flask-mail.readthedocs.io/en/latest/, to send triggered email to business owner when an enquiry is sent
        msg = Message(
            subject=f"Website Enquiry from {fullname}",
            sender=("Duck's Lawn Care Enquiries", "notifications.duck64843@gmail.com"),
            recipients=["duck64843@gmail.com"],
        )
        assert msg.sender == "Duck's Lawn Care Enquiries <notifications.duck64843@gmail.com>"
        msg.html = f"<p>Hi Duck,</p><p>A new enquiry has come through via the <em>Contact Us</em> form on the website.</p><p><strong>Name:</strong> {fullname}<br /><strong>Postcode:</strong> {postcode}<br /><strong>Message:</strong> {enquiry}<br /><strong>Needed by:</strong> {turnaround}<br /><strong>Phone:</strong> {phone}<br /><strong>Email:</strong> {email}<br /><strong>Submitted:</strong> {current_time}<br /></p><p>The client has been notified that they will be contacted in 1-2 business days.</p><p>Thanks,</p><p>Duck's Lawn Care Enquiries</p>"
        mail.send(msg)
        # Upon completion redirect user to the homepage
        return redirect("/")
    else:
        return render_template("contact.html")


def scheduled_email():
    """Scheduled email summaring enquiries received for the day"""
    with app.app_context():
        # Get data for the email (number of enquiries), and anything else
        # Variable for current_day in YYYY-MM-DD format
        # Consulte CS50 AI on how to format time in desired format
        now = datetime.now()
        current_day = now.strftime("%Y-%m-%d")
        # Variable for total enquiries for current day
        total_row = db.execute("SELECT COUNT (*) FROM enquiries WHERE DATE(date) = ?", current_day)
        total = total_row[0]['COUNT (*)']
        print(f"Count of enquiries for the day is {total}")
        # Variable for total enquiries where Urgency = today
        today_row = db.execute(
            "SELECT COUNT (*) FROM enquiries WHERE DATE(date) = ? AND urgency = ?", current_day, 'Today')
        today = today_row[0]['COUNT (*)']
        print(f"Total: {total}")
        # Variable for total enquiries where Urgency = Next few days
        nfd_row = db.execute(
            "SELECT COUNT (*) FROM enquiries WHERE DATE(date) = ? AND urgency = ?", current_day, 'Next few days')
        nfd = nfd_row[0]['COUNT (*)']
        print(f"Next few days: {nfd}")
        # Variable for total enquiries where Urgency = Within the week
        ww_row = db.execute(
            "SELECT COUNT (*) FROM enquiries WHERE DATE(date) = ? AND urgency = ?", current_day, 'Within week')
        ww = ww_row[0]['COUNT (*)']
        print(f"Within the week: {ww}")
        # Variable for total enquiries where Urgency = Not urgent
        noturg_row = db.execute(
            "SELECT COUNT (*) FROM enquiries WHERE DATE(date) = ? AND urgency = ?", current_day, 'Not urgent')
        noturg = noturg_row[0]['COUNT (*)']
        print(f"Not urgent: {noturg}")
        # Variable for total enquiries where Urgency = Other
        other_row = db.execute(
            "SELECT COUNT (*) FROM enquiries WHERE DATE(date) = ? AND urgency = ?", current_day, 'Other')
        other = other_row[0]['COUNT (*)']
        print(f"Other: {other}")
        # # Variable for Total unattended enquiries
        total_un_row = db.execute(
            "SELECT COUNT (*) FROM enquiries WHERE status = ?", 'Not Contacted')
        total_un = total_un_row[0]['COUNT (*)']
        # Send the scheduled email
        # Adapted from: https://flask-mail.readthedocs.io/en/latest/, to send triggered email to business owner when an enquiry is sent
        msg = Message(
            subject=f"Daily Summary of Enquiries {current_day}",
            sender=("Duck's Lawn Care Enquiries", "notifications.duck64843@gmail.com"),
            recipients=["duck64843@gmail.com"],
        )
        assert msg.sender == "Duck's Lawn Care Enquiries <notifications.duck64843@gmail.com>"
        msg.html = f"<p>Hi Duck,</p><p>Here is a summary of the enquiries that came through today via the <em>Contact Us</em> form on the website.</p><h3><strong>Total Enquiries: </strong>{total}</h3><p>Below is a breakdown of when the work is required:</p><p><strong>Today: </strong>{today}<br /><strong>Next few days: </strong>{nfd}<br /><strong>Within the week: </strong>{ww}<br /><strong>Not urgent: </strong>{noturg}<br /><strong>Other: </strong>{other}<br /></p><h3><strong>Total Unattended Enquiries:{total_un}</strong></h3><p>To see the enquiries in more detail please log in to the website.</p><p>Thanks,</p><p>Duck's Lawn Care Enquiries</p>"
        mail.send(msg)


# Scheduled job programmed to run each day at 18:00
# Adapted from: https://apscheduler.readthedocs.io/en/3.x/userguide.html, by Alex Grönholm, used to schedule email send at 6pm each
scheduler.add_job(scheduled_email, 'cron', hour=17, minute=20)
# Interval job that runs every 60 seconds (to be used for testing)
# scheduler.add_job(scheduled_email, 'interval', seconds =60)


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash('Username must be provided.')
            return redirect("/login")
        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('Invalid username or password.')
            return redirect("/login")
        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            flash('Invalid username or password.')
            return redirect("/login")
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = request.form["username"]
        # Redirect user to home page
        return redirect("/staff")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/staff")
@login_required
def staff():
    """Show customer enquiries"""
    # Consulted CS50 AI on possible ways to set up pagination variables to pass back to the rendered webpage
    page = request.args.get('page', 1, type=int)
    per_page = 5
    offset = (page - 1) * per_page
    user_id = session.get("user_id")
    # Retrieve rows for the current range
    rows = db.execute(
        "SELECT * FROM enquiries WHERE user_id = ? ORDER BY date DESC LIMIT ? OFFSET ?", user_id, per_page, offset)
    total_rows_info = db.execute("SELECT COUNT (*) FROM enquiries WHERE user_id = ?", user_id)
    total_rows = total_rows_info[0]['COUNT (*)']
    total_pages = math.ceil(total_rows / per_page)
    # Calculate Start and End for user display, used for age of enquiry
    # Consulted CS50 AI on how I can go about performing this calculation
    start = offset + 1
    end = min(offset + per_page, total_rows)
    # Get the current time
    current_time = datetime.now()
    enquiries = []
    for n in rows:
        enquiry_date = datetime.strptime(n['date'], '%Y-%m-%d %H:%M')
        time_diff = current_time - enquiry_date
        days = time_diff.days
        hours = time_diff.seconds // 3600
        n['age'] = f"{days} days, {hours} hours"
        enquiries.append({
            "age": n['age'],
            "date": n['date'],
            "email": n['email'],
            "id": n['id'],
            "message": n['message'],
            "name": n['name'],
            "notes": n['notes'],
            "phone": n['phone'],
            "postcode": n['postcode'],
            "status": n['status'],
            "urgency": n['urgency'],
        })
    return render_template("staff.html", enquiries=enquiries, page=page, total_pages=total_pages, start=start, end=end, total_rows=total_rows)


@app.route("/update_status", methods=["POST"])
def update_status():
    # Consulted ChatGPT on how to handle the information passed from JavaScript to be able to insert into contactus.DB
    """Update enquiry if button is pressed"""
    if request.method == "POST":
        data = request.get_json()
        if 'row_id' not in data or 'new_status' not in data:
            return jsonify({'success': False, 'error': 'Missing data'}), 400
        print("data: ", data)
        row_id = data['row_id']
        new_status = data['new_status']
        # Execute SQL query to update status
        db.execute("UPDATE enquiries SET status = ? WHERE id = ?", new_status, row_id)
        return jsonify(success=True)
    else:
        return redirect("/staff")


@app.route("/update_note", methods=["POST"])
def update_note():
    """Update or edit a note in the enquiries table."""
    # Consulted ChatGPT on how to handle the information passed from JavaScript to be able to insert into contactus.DB
    if request.method == "POST":
        data = request.get_json()
        if 'row_id' not in data or 'note' not in data:
            return jsonify({'success': False, 'error': 'Missing data'}), 400
        row_id = data['row_id']
        updated_note = data['note']
        # Update the 'notes' column for the corresponding row in the database
        db.execute("UPDATE enquiries SET notes = ? WHERE id = ?", updated_note, row_id)
        return jsonify(success=True)
    else:
        return jsonify(success=False)


@app.route("/logout")
def logout():
    # Adapted from: https://cs50.harvard.edu/x/2024/weeks/9/, which logs a user out
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/login")


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    """Change password for user"""
    user_id = session.get("user_id")
    if request.method == "POST":
        # Flash error message if 'current password' is empty.
        if not request.form.get("current password"):
            flash('Please provide current password')
            return redirect("/change")
        # Flash error message if 'new password' is empty.
        if not request.form.get("new password"):
            flash('Please provide new password')
            return redirect("/change")
        # Flash error message if 'confirmation' is empty.
        if not request.form.get("confirmation"):
            flash('Please confirm password')
            return redirect("/change")
        # Flash error message if the current password is incorrect
        hashed_pw_attempt = request.form.get("current password")
        hashed_pw_row = db.execute("SELECT hash FROM users where id = ?", user_id)
        hashed_pw = hashed_pw_row[0]['hash']
        if len(hashed_pw_row) != 1 or not check_password_hash(hashed_pw, hashed_pw_attempt):
            flash('Incorrect password')
            return redirect("/change")
        # Flash error message if the new passwords do not match.
        elif request.form.get("new password") != request.form.get("confirmation"):
            flash('Passwords do not match')
            return redirect("/change")
        elif check_password_hash(hashed_pw, hashed_pw_attempt) and request.form.get("new password") == request.form.get("confirmation"):
            # Hash the new password, assign it to 'new_hashed_pw'
            new_hashed_pw = generate_password_hash(request.form.get("confirmation"))
            # Update the 'users' table with 'new_hashed_pw'
            db.execute("UPDATE users SET hash = ? WHERE id = ?", new_hashed_pw, user_id)
            flash('Password successfully updated.')
        return redirect("/")
    else:
        # Forget any user_id and redirect user to login form
        return render_template("change.html")
