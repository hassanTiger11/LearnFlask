from flask import Flask, abort
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)


    def __repr__(self):
            return "Video(name = "+self.name+", views= "+str(self.views) +", likes= "+str(self.likes) 


db.create_all()

def abort_if_exist(vid_id):
    result = VideoModel.query.filter_by(id=vid_id)
    if result:
        abort(404, "Video ID exist")

video_put_reqParser = reqparse.RequestParser()
video_put_reqParser.add_argument("name", type=str, help="enter name")
video_put_reqParser.add_argument("likes", type=int, help="enter #likes")
video_put_reqParser.add_argument("views", type=int, help="enter #views")

  

resource_feilds = {
    "id": fields.Integer, 
    "name": fields.String,
    "likes": fields.Integer,
    "views": fields.Integer,
}

class Videos(Resource):
    @marshal_with(resource_feilds)
    def put(self, video_id):
        abort_if_exist(video_id)
        args = video_put_reqParser.parse_args()
        video = VideoModel(id=video_id, name=args["name"], views=args["views"], likes=args["likes"])
        print(video)
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_feilds)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        return result

'''
    def delete(self, video_id):

        del vids[video_id]
        return "deleted "+ str(video_id), 204

'''
api.add_resource(Videos, "/video/<int:video_id>")

