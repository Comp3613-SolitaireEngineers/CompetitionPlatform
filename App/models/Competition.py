from datetime import datetime
from App.database import db

class Competition(db.Model):
    __tablename__ = 'competition'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(120), nullable=False)
    platform = db.Column(db.String(120), nullable=False)
    hosts = db.relationship("CompetitionHost", lazy=True, backref=db.backref("hosts"), cascade="all, delete-orphan")
    participants = db.relationship("Competitor", secondary='results', viewonly=True, back_populates='competitions')
    results = db.relationship('Results', backref='competition', viewonly=True, lazy=True)
    results_added = db.Column(db.Boolean, default=False)


    def __init__(self, name, location, platform, date):
        self.name = name
        self.location = location
        self.platform = platform
        self.date = date

    
    def get_json(self):
        return{
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'platform': self.platform,
            'date': self.date.strftime("%Y-%m-%d %H:%M:%S"),
            "hosts": [host.toDict() for host in self.hosts],
            "participants": [participant.get_json() for participant in self.participants]
        }