from App.models import Command
from App.database import db

def execute_competition_command(self, admin_id, competition_id):
    command = CompetitionCommand(competition_id)
    try:
        command.execute(admin_id, competition_id)
        return "Competition command executed successfully"
    except Exception as e:
        return f"Error executing competition command: {str(e)}"
    
def execute_results_command(self, admin_id, competition_id, results):
    command = ResultsCommand(competition_id)
    try:
        command.execute(admin_id, competition_id, results)
        return "Results command executed successfully"
    except Exception as e:
        return f"Error executing results command: {str(e)}"
