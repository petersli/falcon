from flask import Flask, request, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import boto3, botocore
import os, secrets, json

app = Flask(__name__)
CORS(app)
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
        return prime.api_key
        
@app.route("/api/v1/falcon_create_html", methods=["POST"])
def falcon_create_html():
    data = request.json
    prime = User.query.filter_by(api_key=data["api_key"]).first()
    
    input_type = data["input"].split(".")[0]
    output_type = data["output"].split(".")[0]
    input_shape = data["input"].split(".")[1].split("x")
    output_shape = data["output"].split(".")[1].split("x")
    
    config = {
        "model_url": data["model_url"],
        "code_url": data["model_url"],
        "input_type": input_type,
        "input_channels": input_shape[0],
        "input_width": input_shape[1],
        "input_height": input_shape[2],
        "output_type": output_type,
        "output_channels": input_shape[0],
        "output_width": input_shape[1],
        "output_height": input_shape[2],
    }

    with open("storage/" + data["api_key"] + ".json", 'w') as fp:
        json.dump(config, fp)

    return "Request Accepted. Is it correct? Who knows."

@app.route("/api/v1/falcon_incoming_request", methods=["POST"])
def falcon_incoming_request():
    # data = request.json
    # if data["input_type"] == "image":
    #     file = request.files['file']
    #     filename = secure_filename(file.filename)
    #     file.save(filename))
    # if data["input_type"] == "audio":
    #     file = request.files['file']
    #     filename = secure_filename(file.filename)
    #     file.save(filename))
    # if data["input_type"] == "numbers":
    #     numbers = data["data"]
    # if data["input_type"] == "text":
    #     text = data["input_Text"]
    return "nice one"

@app.route("/tejpal")
def tejpal():

    config = {
        "model_url": "",
        "code_url": "",
        "input_type": "image",
        "input_channels": "3",
        "input_width": "64",
        "input_height": "64",
        "output_type": "64",
        "output_channels": "3",
        "output_width": "64",
        "output_height": "64",
    }


    return render_template("tejpal.html", config=config)

if __name__ == '__main__':
    app.run(debug=True)
    