from flask import Flask, render_template, make_response, request

import setup_db as db

app = Flask(__name__)

class User:
  def __init__(self, username, gender, email, password, admin):
    self.username = username
    self.gender = gender
    self.email = email
    self.password = password
    self.admin = admin

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/register", methods=["GET", "POST"])
def register():
  if request.method == "POST":
    connection = db.create_connection("database.db")

    data = request.form
    username = data["username"]
    gender = data["gender"]
    email = data["email"]
    password = data["password"]
    admin = 0
    
    new_user = User(username, gender, email, password, admin)
    db.register(connection, new_user)
    
  return render_template('register.html')

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    connection = db.create_connection("database.db")

    data = request.form
    username = data["username"]
    password = data["password"]
    
    login = db.login(connection, username, password)
    
    if login:
      response = make_response(render_template('index.html'))
      response.set_cookie("cookie", username)
      return response
    else:
      print("Failed to login")

  return render_template('login.html')

if __name__ == '__main__':
	app.run(debug=True)