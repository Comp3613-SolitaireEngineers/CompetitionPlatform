from App.database import db
from .User import User
from .Rank import Rank

class Competitor(User):
    __tablename__ = 'competitor'  
    
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)      
    rank = db.relationship('Rank', uselist=False, lazy=True)
    competitions = db.relationship('Competition', secondary='results', back_populates='participants', viewonly=True)       
    notifications = db.relationship('Notification', backref='competitor', lazy=True)
    
    def __init__(self, uwi_id, username,email,password, firstname, lastname):
        super().__init__(uwi_id, username,email, password)        
        self.firstname = firstname
        self.lastname = lastname
        self.user_type = 'competitor'
        self.rank = Rank(self.id)


    def __repr__(self):       
        return f"<Competitor {self.id}, {self.uwi_id} , {self.firstname}, {self.lastname}, {self.username}, {self.rank}>"

    def get_json(self):
        return {
            'id': self.id,
            'uwi_id': self.uwi_id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'username': self.username,
            'rank': self.rank.get_json() if self.rank else "",
            # 'competitions': [comp.get_json() for comp in self.competitions] if self.competitions else [],
            #'notifications': [notification.toDict() for notification in self.notifications] if self.notifications else [],
            'role' : 'competitor'            
        }
