from App.database import db

class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String, nullable=False, unique=True)
    website = db.Column(db.String, nullable=True)
    
    competitions = db.relationship("CompetitionHost", lazy=True, backref=db.backref("competitions"), cascade="all, delete-orphan")

    def __init__(self, name, website):
        self.name = name
        self.website = website

    def toDict(self):
        res = {
            "id": self.id,
            "name": self.name,
            "website": self.website
        }
        return res