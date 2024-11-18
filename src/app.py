import json
from db import db
from flask import Flask, request
from db import LaundryTime, User, Laundry, Dorm

app = Flask(__name__)
db_filename = "laundry.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error": message}), code

# your routes here
@app.route("/")
def hello_world():
    return "Hello world!"

@app.route("/api/users/")
def get_users():
    """
    Endpoint for getting all users
    """
    return success_response({"users" : [t.serialize() for t in User.query.all()]})

@app.route("/api/users/", methods = ["POST"])
def create_user():
    """
    Endpoint for creating a new user
    """
    body = json.loads(request.data)
    name = body.get("name", None)
    netid = body.get("netid", None)
    balance = body.get("balance", 0)
    if name is None:
        return failure_response("Invalid input: User's name is not provided", 400)
    if netid is None:
        return failure_response("Invalid input: User's netid is not provided", 400)
    new_user = User(
        name = name,
        netid = netid,
        balance = balance
    )
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)

@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    """
    Endpoint for getting a user
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    return success_response(user.serialize())

@app.route("/api/users/<int:user_id>/", methods = ["DELETE"])
def delete_user(user_id):
    """
    Endpoint for deleting user
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    x = user.serialize()
    db.session.delete(user)
    db.session.commit()
    return success_response(x)

@app.route("/api/dorms/")
def get_dorms():
    """
    Endpoint for getting all dorms
    """
    return success_response({"dorms" : [t.serialize() for t in Dorm.query.all()]})

@app.route("/api/dorms/", methods = ["POST"])
def create_dorm():
    """
    Endpoint for creating a new dorm
    """
    body = json.loads(request.data)
    dorm = body.get("dorm", None)
    if dorm is None:
        return failure_response("Invalid input: Dorm's name is not provided", 400)
    new_dorm = Dorm(
        dorm = dorm
    )
    db.session.add(new_dorm)
    db.session.commit()
    return success_response(new_dorm.serialize(), 201)

@app.route("/api/dorms/<int:dorm_id>/")
def get_dorm(dorm_id):
    """
    Endpoint for getting a dorm
    """
    dorm = Dorm.query.filter_by(id=dorm_id).first()
    if dorm is None:
        return failure_response("Dorm not found")
    return success_response(dorm.serialize())

@app.route("/api/dorms/<int:dorm_id>/", methods = ["DELETE"])
def delete_dorm(dorm_id):
    """
    Endpoint for deleting dorm
    """
    dorm = Dorm.query.filter_by(id=dorm_id).first()
    if dorm is None:
        return failure_response("Dorm not found")
    x = dorm.serialize()
    db.session.delete(dorm)
    db.session.commit()
    return success_response(x)

@app.route("/api/users/<int:user_id>/<int:laundry_id>/add/", methods = ["POST"] )
def add_laundry_to_user(user_id, laundry_id):
    """
    Endpoint for adding a new laundry to a user
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    body = json.loads(request.data)
    duration = body.get("duration", None)
    laundry = Laundry.query.filter_by(id=laundry_id).first()
    if laundry is None:
        return failure_response("Laundry not found")
    if duration is None:
        return failure_response("Invalid input: Laundry's duration is not provided", 400)
    user_balance = user.balance
    laundry_cost = laundry.cost
    if user_balance < laundry_cost:
        return failure_response("Laundry's cost exceeds user's current balance", 403)
    user.balance -= laundry_cost
    new_laundry_time = LaundryTime(
        laundry_id = laundry_id,
        duration = duration,
        user_id = user_id
        )
    db.session.add(new_laundry_time)
    db.session.commit()
    return success_response(new_laundry_time.serialize(), 201)

@app.route("/api/laundry/<int:laundry_id>/")
def get_laundry_for_user(laundry_id):
    """
    Endpoint for getting information of laundry based on the user
    """
    laundry = Laundry.query.filter_by(id=laundry_id).first()
    if laundry is None:
        return failure_response("Laundry not found")
    if laundry.laundry_time == []:
        return success_response(laundry.serialize())
    laundry_with_time = LaundryTime.query.filter_by(laundry_id=laundry_id).first()
    return success_response(laundry_with_time.serialize())


@app.route("/api/laundries/<int:dorm_id>/", methods = ["POST"])
def create_a_laundry(dorm_id):
    """
    Endpoint for creating a laundry
    """
    body = json.loads(request.data)
    dorm = Dorm.query.filter_by(id=dorm_id).first()
    if dorm is None:
        return failure_response("Dorm not found")
    laundry_number = body.get("laundry_number", None)
    laundry_type = body.get("laundry_type", None)
    if laundry_number is None:
        return failure_response("Invalid input: Laundry's number is not provided", 400)
    if laundry_type is None:
        return failure_response("Invalid input: Laundry's type is not provided", 400)
    if laundry_type == ("washer" or "Washer"):
        cost = 1.75
    else:
        cost = 1.30
    new_laundry = Laundry(
        dorm_id = dorm_id,
        laundry_number = laundry_number,
        laundry_type = laundry_type,
        cost = cost
    )
    db.session.add(new_laundry)
    db.session.commit()
    return success_response(new_laundry.serialize(), 201)

@app.route("/api/users/<int:user_id>/transactions/", methods = ["POST"])
def create_transaction(user_id):
    """
    Endpoint for updating user's balance
    """
    body = json.loads(request.data)
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    amount = body.get("amount", None)
    if amount is None:
        return failure_response("Invalid input: Amount is not provided", 400)
    user.balance += amount
    db.session.commit()
    return success_response(user.serialize(), 201)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
