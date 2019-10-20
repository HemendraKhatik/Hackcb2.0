import os
from flask import Flask, session, render_template, request, url_for,redirect, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
# DATABASE_URL="postgres://wlaxxoqfdmuoxx:60b3846db4ce73d5595e5510808f20788865242be016bc20a34ebcacc4dab6fd@ec2-54-235-104-136.compute-1.amazonaws.com:5432/denacruri026b6"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
	return render_template("landing.html")

@app.route("/home")
def home():
	return render_template("home.html")

@app.route("/html")
def html():
	return render_template("html.html")

@app.route("/github")
def github():
	return render_template("github.html")
	
@app.route("/signup",methods=["POST","GET"])
def signup():
	if request.method == "GET":
		return render_template("signup.html")
	email=request.form.get("email")
	check_email=db.execute("SELECT * FROM signup WHERE email=:email",
		{"email":email}).fetchall()
	# email validation 
	if check_email:
		flash("Email address already used!")
		return redirect(request.url)
	# password confirmation 
	if request.form.get("password") != request.form.get("c_password"):
		flash("Password does not match!")
		return redirect(request.url)
	password = request.form.get("c_password");	
	db.execute("INSERT INTO signup(email,password) VALUES(:email,:password)",
	{"email":email,"password":password})
	db.commit()
	db.close()
	return render_template("login.html")

@app.route("/login",methods=["POST","GET"])
def login():
	if request.method == "GET":
		return render_template("login.html")
	email=request.form.get("email")
	password=request.form.get("password")
	query=db.execute("SELECT * FROM signup WHERE email=:email AND password=:password",
		{"email":email,"password":password}).fetchall()
	for q in query:
		if q.email==email and q.password==password:
			return render_template("home.html")
	flash("Invalid email or password!")
	return redirect(request.url)				

@app.route("/logout")
def logout():
	return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)	