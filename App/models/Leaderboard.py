from App.database import db

class Leaderboard(LeaderBoardPublisher):

    def __init__(self):
        self._observers = []
        self._ranking_history = []

    def register(self, observer):
        self._observers.append(observer)
    
    def detach(self, observer):
        self._observers.remove(observer)

    def notify_observer(self):
        for observer in self._observers:
            observer.update(self._leaderboard)

    def log_ranking_history(self, user_id, ranking):
        self._ranking_history.append((user_id, ranking))

    def get_ranking_history(self):
        return self._ranking_history
    
    def get_ranking_history_by_user(self, user_id):
        return [user_ranking_history for user, ranking in self._ranking_history if user == user_id]