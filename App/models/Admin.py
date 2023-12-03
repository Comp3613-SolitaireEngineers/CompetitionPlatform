from App.database import db
from App.models import User
from App.models import Results
from App.models import Rank, Competition

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
        
    def add_competition(self, competition):
        db.session.add(competition)
        db.session.commit()

    def create_competition(self, name, location, platform, date): 
        try:
            newcomp = Competition.Competition(name = name, location = location,platform = platform, date = date)
            db.session.add(newcomp)
            db.session.commit()
            return newcomp
        except Exception as e:
            print("Error in competition in model ", e)
            db.session.rollback()
            return None

    def update_ranks(self):
        # Get all users
        users = User.query.all()

        # Calculate the total points for each user
        for user in users:
            total_points = 0
            for user_competition in user.competitions:
                # Here we're giving 50 points for participation and additional points based on the rank
                points = 50 + (100 - user_competition.rank)
                total_points += points

            # Update the user's rank
            rank = Rank.query.filter_by(user_id=user.id).first()
            if rank:
                rank.points = total_points
            else:
                rank = Rank(user_id=user.id, points=total_points)
                db.session.add(rank)
        db.session.commit()