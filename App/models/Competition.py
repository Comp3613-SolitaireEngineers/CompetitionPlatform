from datetime import datetime
from App.database import db

class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(120), nullable=False)
    hosts = db.relationship("CompetitionHost", lazy=True, backref=db.backref("hosts"), cascade="all, delete-orphan")
    participants = db.relationship("Competitor", secondary='usercompetition', back_populates='competitions')


    def __init__(self,id, name, location):
        self.id = id
        self.name = name
        self.location = location


    
    def get_json(self):
        return{
            'id': self.id,
            'name': self.name,
            'location': self.location
        }



    def toDict(self):
        res = {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "location": self.location,
            "hosts": [host.toDict() for host in self.hosts],
            "participants": [participant.toDict() for participant in self.participants]
        } 
        return res
