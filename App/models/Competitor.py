from App.database import db
from .User import User
from .Notification import Notification
from .Rank import Rank

class Competitor(User):
    __tablename__ = 'competitor'  
    
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)      
    rank = db.relationship('Rank', uselist=False, lazy=True)
    competitions = db.relationship('Competition', secondary='results', back_populates='participants', viewonly=True)       
    notifications = db.relationship('Notification', backref='competitor', lazy=True)
    top_observer_id = db.Column(db.Integer, db.ForeignKey('rank_top_observers.id')) #, nullable=False)
    
    def __init__(self, uwi_id, username,email,password, firstname, lastname):
        super().__init__(uwi_id, username,email, password)        
        self.firstname = firstname
        self.lastname = lastname
        self.user_type = 'competitor'
        # Create a new Rank instance and associate it with this Competitor
        self.set_rank()
        


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
            'platform_rank': self.rank.get_json() if self.rank else "",
            'role' : 'competitor'            
        }

    def set_rank(self):
        try:
            self.rank = Rank(self.id)
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            return False

    def update_notifications(self, message, title):
        try:
            notification = (Notification(self.id, message, title))
            db.session.add(notification)
            db.session.commit()   
            print(f'Competitor {self.username} received message: {message}')        
        except Exception as e:
            print("Exception when updating notifications " + str(e))
