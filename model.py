from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin


app = Flask(__name__)
app.secret_key = "SECRETKEY"

db = SQLAlchemy()
#################################################################################

#Defining each table through classes 

class PollingCenter(db.Model):
    """Table containing polling center's information"""

    __tablename__ = "pollingcenters"

    polling_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True)
    # address = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    hours_of_operation = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Human readable representation of data from PollingCenter table"""

        return f"""<Polling Center polling_id={self.polling_id} 
                                address={self.address} 
                                hours_of_operation={self.hours_of_operation}>"""

class PollingHour(db.Model):
    """Table containing polling center's hours of operation based on state"""

    __tablename__ = "pollinghours"

    state_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    state_name = db.Column(db.String, nullable=False)
    state_abbrev = db.Column(db.String, nullable=False)
    state_hours = db.Column(db.String, nullable=False)
    
    def __repr__(self):
        """Human readable representation of data from PollingHour table"""

        return f"""<PollingHour state_id={self.state_id} 
                            state_name={self.state_name} 
                            state_hours={self.state_hours}>"""

class Comment(db.Model):
    """Table containing User's comments for each Polling Center"""

    __tablename__ = "comments"

    comment_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    polling_id = db.Column(db.Integer, db.ForeignKey('pollingcenters.polling_id'), nullable=False)
    comment = db.Column(db.String(140), nullable=False)

    #Defining relationship between Comment and Polling Center tables
    polling_center = db.relationship("PollingCenter",
                                    backref=db.backref("comments", order_by=user_id))

    #Defining relationship between Comment and User table
    user = db.relationship("User",
                            backref=db.backref("comments", order_by=comment_id))

    def __repr__(self):
        """Human readable representation of data from Comments table"""

        return f"""<Comment comment_id={self.comment_id} 
                            user_id={self.user_id} 
                            polling_id={self.polling_id}>"""

class User(UserMixin, db.Model):
    """Table containing User's profile information"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    
    party_id = db.Column(db.Integer, db.ForeignKey('parties.party_id'), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    state = db.Column(db.Integer, db.ForeignKey('pollinghours.state_id'), nullable=False)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    phonenum = db.Column(db.String(10), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)

    #Defining relationship between User and Comment table
    comment = db.relationship("Comment",
                            backref=db.backref("users", order_by=id))
    
    #Defining relationship between User and Parties table
    parties = db.relationship("Parties",
                            backref=db.backref("users", order_by=id))

    pollinghours = db.relationship("PollingHour",
                                    backref=db.backref("users", order_by=id))

    # def set_password(self, password):
    #     """create hashsed password"""
    #     self.password_hash = generate_password_hash(password)
    
    # def check_password(self, password):
    #     """checks hashes password"""
    #     return check_password_hash(self.password, password)

    def __repr__(self):
        return f"""<User user_id={self.id} party_id={self.party_id}>"""


class Parties(db.Model):
    """Table containing each political party"""

    __tablename__ = "parties"

    party_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    
    political_party = db.Column(db.String(100), nullable=False)
    political_party_abbr = db.Column(db.String(4), nullable=False)

    #Defining relationship between Parties and Political Candidates tables
    # candidates = db.relationship("PoliticalCandidates",
    #                             backref=db.backref("parties", order_by=party_id))

    def __repr__(self):
        return f"<Parties party_id={self.party_id}>"

# class PoliticalCandidates(db.Model):
#     """Table containing each political candidates information"""

#     __tablename__ = "politicalcandidates"

#     candidate_id = db.Column(db.Integer,
#                             primary_key=True, 
#                             autoincrement=True)
#     party_id = db.Column(db.Integer, db.ForeignKey('parties.party_id'), nullable=False)
#     candidate_name = db.Column(db.String(150), nullable=False)
#     description = db.Column(db.String(400), nullable=False)

#     def __repr__(self):
#         """Return human-readable representation of Political Candidates Table"""
#         return f"<Political Candidates party_id={self.party_id} candidate_name={self.candidate_name}>"   

##############################################################################
#Helper Functions

def connect_to_db(app):
    """Connects the database to our Flask app"""

    #Configures app to use our database
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///votings"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # from server import app
    connect_to_db(app)
