from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import africastalking

db = SQLAlchemy()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

db.init_app(app)
CORS(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phoneno = db.Column(db.Integer,nullable=False)
    tax_id = db.Column(db.String, unique=True, nullable=False)

with app.app_context():
    db.create_all()

@app.post("/")
def index():
    return "Welcome to Taxify"

@app.post("/pay")
def pay_tax():
    name = request.json.get("name")
    phoneno = request.json.get("phoneno")
    tax_id = request.json.get("tax_id")
    user = User(name=name,phoneno=phoneno,tax_id=tax_id)
    db.session.add(user)
    message = f"Dear {name},Congratulations on successfully making your tax payment! Now it's time to take control of where your hard-earned money goes.Introducing Taxify, the revolutionary app that puts the power in your hands. By clicking the link below, you'll unlock the ability to allocate your tax payment to sectors that matter most to you. It's a chance to shape the future of our economy![Personalized Link: www.taxifyapp.com/allocate?user=example123]"
    username = "EmojiSwap"    
    api_key = "c65988c74e21c3fd6c742f7ff46df5d737157cf440a8db3b6265862222e8194b"     
    africastalking.initialize(username, api_key)

    sms = africastalking.SMS

    response = sms.send(message,[phoneno])
    print(response)
    return 'message sent successfully',20


if __name__ =="__main__":
    app.run()