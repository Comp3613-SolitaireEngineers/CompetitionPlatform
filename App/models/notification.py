from datetime import datetime
from App.database import db

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    competitor_id = db.Column(db.Integer, db.ForeignKey('competitors.id'))
    message = db.Column(db.String)
    timeStamp=db.Column(db.DateTime,defualt = datetime.utcnow)

    
    def __init(self,competitor_id, message, timeStamp):
        self.competitor_id = competitor_id
        self.message = message
        self.timeStamp = timeStamp or datetime.utcnow()
    
    def toDict(self):
     return{
         'id':self.id,
         'competitor_id': self.competitor_id,
         'message': self.message,
         'timeStamp': self.timestamp.isoformat()
     }