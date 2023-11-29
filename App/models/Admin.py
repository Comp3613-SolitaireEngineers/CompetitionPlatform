from App.database import db
from App.models import User
from App.models import UserCompetition
from App.models import Rank

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
            'password': self.password,
            'role' : 'admin'
        }
        
    def add_competition(self, competition):
        db.session.add(competition)
        db.session.commit()

    def add_results(self, competition, results):
        # Add results to the competition
        for user_id, rank in results:
            user_competition = UserCompetition.query.filter_by(comp_id=competition.id, user_id=user_id).first()
            if user_competition:
                user_competition.rank = rank
            else:
                user_competition = UserCompetition(comp_id=competition.id, user_id=user_id, rank=rank)
                db.session.add(user_competition)
        db.session.commit()

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