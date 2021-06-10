'''
This is the fourth api in the sequence for learning flask REST apis
I will look into how I can integrate marshmallow for serilaizationa and deserialization
and I will integrate the swagger library to see how I will be able to share my documentation
'''
from flask import Flask, jsonify, request, abort
from flask_restful import Api, Resource, reqparse
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import requests
from werkzeug.sansio.response import Response

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///myDB.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reward_name = db.Column(db.String(100))
    user = db.relationship('User', backref= 'Rewards')


class userSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
    id = ma.auto_field()
    name = ma.auto_field()
    Rewards = ma.HyperlinkRelated("static")

    
class rewardSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reward

def seperateRequest(name):
    print("\n\n\n------------"+name+"-------------\n\n\n")
logParser = reqparse.RequestParser()
logParser.add_argument("name", type=str, help = "enter name")
class Log(Resource):
    def put(self):
        args = logParser.parse_args()
        user = User(name = args.name)
        db.session.add(user)
        db.session.commit()
        conJson = userSchema()
        result = conJson.dump(user)
        seperateRequest("put")
        return result, 200

    def post(self):
        myUser = User.query.filter_by(name = request.form["name"]).first()
        print("found user...") if myUser else abort("user not found")
        reward = Reward(user= myUser,
                     reward_name= request.form["reward"])
        print("made reward") if reward else abort("couldn't make reward")
        db.session.add(reward)
        db.session.commit()
        seperateRequest("post")
        return 200



    def get(self):
        user = User.query.all()
        userConvJson = userSchema(many= True)
        result =userConvJson.dump(user)
        seperateRequest("get")
        return jsonify({"users": result})
api.add_resource(Log, "/log")

'''
@app.route("/")
def index():
    user1 = User.query.all()
    user_schema = userSchema(many=True)
    output = user_schema.dump(user1)
    return jsonify({'user':output})

@app.route("/push")
def pushUser():
    user = User( name="jeff")
    db.session.add(user)
    db.session.commit()
    return user.name, 200
@app.route("/get")
def getUser():
    user = User.query.filter_by(id= 2).first().name
    return user
'''
if __name__== "__main__":
    app.run(debug=True)