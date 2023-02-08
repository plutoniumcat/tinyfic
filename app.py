from flask import Flask, jsonify
app = Flask(__name__)

from flask_marshmallow import Marshmallow
ma = Marshmallow(app)

from flask_sqlalchemy import SQLAlchemy 

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://tinyfic_admin:12345@localhost:5432/tinyfic_db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

@app.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")


@app.cli.command("seed")
def seed_db():
    from datetime import date
    user1 = User(
        # set the attributes
        email = "test@test.com",
        password = "12345",
        profile = "This user has not created a profile.",
        username = "test_user",
        userpic = "default.png",
        date = date.today()
    )
    # Add the object as a new row to the table
    db.session.add(user1)

    # commit changes
    db.session.commit()
    print("Table seeded") 


@app.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped") 

class User(db.Model):
    # define the table name for the db
    __tablename__= "USERS"
    # Set the primary key
    id = db.Column(db.Integer,primary_key=True)
    # Add the rest of the attributes.
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    profile = db.Column(db.String(500), nullable=True)
    userpic = db.Column(db.String(500), nullable=True)
    date = db.Column(db.Date())

#create Schema with Marshmallow, it will provide the serialization needed for converting the data into JSON
class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "email", "password", "profile", "userpic", "date")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route("/")
def hello():
  return "Hello World!"

  
@app.route("/users", methods=["GET"])
def get_users():
    # get all the users from the database table
    users_list = User.query.all()
    # Convert the cards from the database into a JSON format and store them in result
    result = users_schema.dump(users_list)
    # return the data in JSON format
    return jsonify(result)