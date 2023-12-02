from datetime import datetime
from App.database import db

class Notification(db.Model):
    __tablename__ = 'notification'
    
    id = db.Column(db.Integer, primary_key=True)
    competitor_id = db.Column(db.Integer, db.ForeignKey('competitor.id'))
    message = db.Column(db.String(220))
    timestamp=db.Column(db.DateTime,default = datetime.now())
    seen = db.Column(db.Boolean, default=False)


    def __init__(self, competitor_id, message):
        self.competitor_id = competitor_id
        self.message = message
        
    
    def toDict(self):
     return{
         'id':self.id,
         'competitor_id': self.competitor_id,
         'message': self.message,
         'timestamp': self.timestamp.strftime("%m/%d/%Y, %H:%M:%S") if self.timestamp else None
     }
