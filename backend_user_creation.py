import os

from cs50 import SQL

from werkzeug.security import check_password_hash, generate_password_hash

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///contactus.db")

username = "duckboss"
pwd = "Vazquez2002"
hashed_pwd = generate_password_hash(pwd)
try:
    db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
               username, hashed_pwd)
    print("User added successfully.")

except ValueError:
    print("Username already exists. Operation failed.")
