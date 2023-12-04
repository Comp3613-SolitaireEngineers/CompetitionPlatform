from App.database import db
from App.models import User
from App.models import Results
from App.models import Rank
from App.models.Competition import Competition

class Admin(User):
    __tablename__ = 'admin'

    def __init__(self, uwi_id, username, email, password):
        super().__init__(uwi_id,username,email, password)        
        self.user_type = 'admin'

    def get_json(self):
        return{
            'id': self.id,
            'uwi_id': self.uwi_id,
            'email': self.email,
            'username': self.username,
            'role' : 'admin'
        }
        
    def create_competition(self, name, location, platform, date): 
        try:
            newcomp = Competition(name = name, location = location,platform = platform, date = date)
            db.session.add(newcomp)
            db.session.commit()
            return newcomp
        except Exception as e:
            print("Error in competition", e)
            db.session.rollback()
            return None