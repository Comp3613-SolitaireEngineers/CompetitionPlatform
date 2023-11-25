from datetime import datetime
from App.database import db

class Notification(db.Model):
    __tablename__ = 'notification'
    
    id = db.Column(db.Integer, primary_key=True)
    competitor_id = db.Column(db.Integer, db.ForeignKey('competitor.id'))
    message = db.Column(db.String)
    timeStamp=db.Column(db.DateTime,defualt = datetime.utcnow)
    
    def toDict(self):
     return{
         'id':self.id,
         'competitor_id': self.competitor_id,
         'message': self.message,
         'timeStamp': self.timestamp.isoformat()
     }