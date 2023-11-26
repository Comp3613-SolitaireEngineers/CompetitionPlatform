from App.database import db, abstractmethod

class Command(db.Model):
    
    @abstractmethod
    def get_json(self):
        pass
    
    @abstractmethod
    def toDict(self):
        pass
    
    @abstractmethod
    def execute(self, admin_id, competition_id):
        pass


# from App.database import db

# class Command(db.Model):
#     __abstract__ = True
#     __tablename__ = 'command'
#     id = db.Column(db.Integer, primary_key=True)
#     execute_at = db.Column(db.DateTime, default=datetime.utcnow)

#     def __init__(self, execute_at):
#         self.execute_at = execute_at

#     def get_json(self):
#         return{
#             'id': self.id,
#             'execute_at': self.execute_at
#         }
    
#     def __repr__(self):       
#         return f"<Command {self.id}, {self.execute_at}>"