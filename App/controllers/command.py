from App.models import Command, CompetitionCommand, ResultsCommand, RankCommand, UpdateRanksCommand, PointsCommand, Admin
from App.database import db

def create_competition_command(self, competition_id):
    command = CompetitionCommand(competition_id)
    
    try:
        db.session.add(command)
        db.session.commit()
        return command
    except Exception as e:
        print (f"Error creating competition : {str(e)}")
        
    return None
    
def execute_competition_command(self, admin_id, competition_id):
    
    admin = Admin.query.get(admin_id)
    command = CompetitionCommand(competition_id)
    try:
        command.execute(admin_id, competition_id)
        return "Competition command executed successfully"
    except Exception as e:
        return f"Error executing competition command: {str(e)}"

def get_competition_command_by_id(command_id):
    command = CompetitionCommand.query.get(command_id)
    return command

def get_results_command_by_id(command_id):
    command = ResultsCommand.query.get(command_id)
    return command


def get_competition_command_by_id_json(command_id):
    command = get_competition_command_by_id(command_id)
    if not command:
        return []
    return command.get_json()

def get_results_command_by_id_json(command_id):
    command = get_results_command_by_id(command_id)
    if not command:
        return []
    return command.get_json()


def get_all_competition_commands():
    commands = CompetitionCommand.query.all()
    return commands

def get_all_results_commands():
    commands = ResultsCommand.query.all()
    return commands


def get_all_competition_commands_json():
    commands = get_all_competition_commands()
    return [command.get_json() for command in commands]

def get_all_results_commands_json():
    commands = get_all_results_commands()
    return [command.get_json() for command in commands]