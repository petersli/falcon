from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os, secrets

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.getcwd() + "/database.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    api_key = db.Column(db.String(80), unique=True, nullable=False)
    model_url = db.Column(db.String(80))
    script_url = db.Column(db.String(80))
    config = db.Column(db.String(120))

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/')
def index():
    return os.getcwd()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        data = request.json
        prime = User.query.filter_by(username=data["username"]).first()
        if prime.password == data["password"]:
            return "Authenticated"
        else:
            return "Unauthorized"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        data = request.json
        prime = User(username=data["username"], password=data["password"])
        prime.api_key = secrets.token_hex(5)
        db.session.add(prime)
        db.session.commit()
        return "Success. Check DB."
        
@app.route("/api/v1/falcon", methods=["POST"])
def falcon_submit():
    data = request.json
    print(data["api_key"])
    return data




if __name__ == '__main__':
    app.run(debug=True)
    