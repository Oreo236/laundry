from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from datetime import datetime
# your classes here
class User(db.Model):
    """
    User Model
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    netid = db.Column(db.String, nullable = False)
    balance = db.Column(db.Integer, nullable = False)
    laundry = db.relationship("LaundryTime", cascade = "delete",)

    def __init__(self, **kwargs):
        """
        Initialize Course object/entry
        """
        self.name = kwargs.get("name", "")
        self.netid = kwargs.get("netid", "")
        self.balance = kwargs.get("balance", "")

    
    def serialize(self):
        """
        Serialize a course object 
        """
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid,
            "balance": self.balance,
            "laundry":[s.serialize() for s in self.laundry]

        }
    
    def sim_serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid,
            "balance": self.balance
        }
 

    
class LaundryTime(db.Model):
    """
    Laundry Time Model
    """
    __tablename__ = "laundriestime"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    laundry_id = db.Column(db.Integer, db.ForeignKey("laundries.id"), nullable = False)
    start_time = db.Column(db.Integer, nullable = False)
    duration = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

    def __init__(self, **kwargs):
        """
        Initialize Laundry object/entry
        """
        self.laundry_id = kwargs.get("laundry_id")
        self.start_time =  datetime.now()
        self.duration = kwargs.get("duration", "")
        self.user_id = kwargs.get("user_id")

    def serialize(self):
        """
        Serialize a laundry time object 
        """
        return {
            "id": self.id,
            "laundry": Laundry.query.filter_by(id=self.laundry_id).first().sim_serialize(),
            "start_time": self.start_time,
            "duration": self.duration,
            "user": User.query.filter_by(id=self.user_id).first().sim_serialize()
        }


class Laundry(db.Model):
    """
    Laundry Model
    """
    __tablename__ = "laundries"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    dorm_id = db.Column(db.Integer, db.ForeignKey("dorms.id"), nullable = False)
    laundry_number = db.Column(db.Integer, nullable = False)
    laundry_type = db.Column(db.String, nullable = False)
    cost = db.Column(db.Integer, nullable = False)
    laundry_time = db.relationship("LaundryTime", cascade = "delete",)

    def __init__(self, **kwargs):
        """
        Initialize Laundry object/entry
        """
        self.dorm_id = kwargs.get("dorm_id")
        self.laundry_number = kwargs.get("laundry_number", "")
        self.laundry_type = kwargs.get("laundry_type", "")
        self.cost = kwargs.get("cost", "")

    
    def serialize(self):
        """
        Serialize a laundry object 
        """
        return {
            "id": self.id,
            "dorm": Dorm.query.filter_by(id=self.dorm_id).first().sim_serialize(),
            "laundry_number": self.laundry_number,
            "laundry_type": self.laundry_type,
            "cost" : self.cost,
            "laundry_time":[s.serialize() for s in self.laundry_time]

        }
    
    def sim_serialize(self):
        return {
            "id": self.id,
            "laundry_number": self.laundry_number,
            "laundry_type": self.laundry_type,
            "cost": self.cost
        }

class Dorm(db.Model):
    """
    Dorm Model
    """
    __tablename__ = "dorms"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    dorm = db.Column(db.String, nullable = False)
    laundry = db.relationship("Laundry", cascade = "delete",)
    
    def __init__(self, **kwargs):
        """
        Initialize Dorm object/entry
        """
        self.dorm = kwargs.get("dorm", "")

    def serialize(self):
        """
        Serialize a laundry object 
        """
        return {
            "id": self.id,
            "dorm": self.dorm,
            "laundry":[s.serialize() for s in self.laundry]
        }
    
    def sim_serialize(self):
        return {
            "id": self.id,
            "dorm": self.dorm
        }