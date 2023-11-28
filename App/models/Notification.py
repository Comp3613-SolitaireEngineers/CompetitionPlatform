from App.database import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notification'
    
    id = db.Column(db.Integer, primary_key=True)
    competitor_id = db.Column(db.Integer, db.ForeignKey('competitor.id'))
    message = db.Column(db.String(255))    
    timeStamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def toDict(self):
     return{
         'id':self.id,
         'competitor_id': self.competitor_id,
         'message': self.message,
         'timeStamp': self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
     }