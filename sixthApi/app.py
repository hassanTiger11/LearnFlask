'''
After a day of looking up stuff:
    Here is how to establish a connection with a database &
    insert data as object & retreve data as JSON objects
In this api I am using:
    sqlalchemy as an ORM to communicate with the data base
    marshmallow to serialize (ORM->python primitives) or deserialize (python primitive -> ORM)
    flask to establish the api
'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from flask import *
from marshmallow_sqlalchemy import *
from flask_sqlalchemy import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __repr__(self):
        return "<Author(name={self.name!r})>".format(self=self)
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author= relationship("Author", backref = backref("books"))

db.create_all()

class AuthorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Author
        include_relationships = True
        load_instance = True


class BookSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        include_fk = True
        load_instance = True

'''
author = Author(name="Chuck Paluhniuk")
author_schema = AuthorSchema()
book = Book(title="Fight Club", author=author)
db.session.add(author)
db.session.add(book)
db.session.commit()
'''
@app.route("/pushAuthor", methods=["PUT", "POST"])
def pushAuthor():
    author = Author(name = request.form["name"])
    db.session.add(author)
    db.session.commit()
    return "pushed "+ request.form["name"], 200

@app.route("/pushBook/<string:authName>", methods=["PUT", "POST"])
def pushBook(authName):
    auth = Author.query.filter_by(name = authName)
    if auth is None:
        abort("enter author first")
    book = Book(title = request.form["title"])
    db.session.add(book)
    db.session.commit()
    return "pushed "+ request.form["title"],200


@app.route("/getall")
def getAll():
    auth = Author.query.all()
    authSchema = AuthorSchema(many=True)
    result = authSchema.dump(auth)
    return jsonify(result), 200


'''
dump_data = author_schema.dump(author)
print(dump_data)
# {'id': 1, 'name': 'Chuck Paluhniuk', 'books': [1]}

load_data = author_schema.load(dump_data, session=db.session)
print(load_data)
# <Author(name='Chuck Paluhniuk')>
'''
if __name__== "__main__":
    app.run(debug=True)