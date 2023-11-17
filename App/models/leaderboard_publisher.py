from App.database import db

class LeaderBoardPublisher(db.Model):
    
    @abstractmethod
    def register(self,observer):
        pass
    
    @abstractmethod
    def detach(self, observer):
        pass
    
    @abstractmethod
    def notify_observer(self):
        pass