from App.models import Command, CompetitionCommand, ResultsCommand, RankCommand, UpdateRanksCommand, PointsCommand, Admin, Competition
from App.database import db
from App.controllers import create_competition

def create_competition_command(admin_id, name, location, platform, date):
    
    competition = create_competition(admin_id, name, location, platform, date)
    
    if competition:
        command = CompetitionCommand.CompetitionCommand(competition.id)
    
        try:
            db.session.add(command)
            db.session.commit()
            return command
        except Exception as e:
            print (f"Error creating competition : {str(e)}")
        
    return None
    
def execute_competition_command(admin_id, name, location, platform, date):
    
    command = create_competition_command(admin_id, name, location, platform, date)
    try:
        command.execute(admin_id, (Competition.query.get(command.competition_id)))
        return "Competition command executed successfully"
    except Exception as e:
        return f"Error executing competition command: {str(e)}"
    
def create_results_command(competition_id):
    command = ResultsCommand.ResultsCommand(competition_id)
    
    try:
        db.session.add(command)
        db.session.commit()
        return command
    except Exception as e:
        print( f"Error executing results command: {str(e)}")
        return None
    
def execute_results_command(admin_id, competition_id, results_file_path):
    
    admin = Admin.query.get(admin_id)
    
    if admin:
        command = create_results_command(competition_id)
        if command:
            try:
                command.execute(admin_id, competition_id, results_file_path)
                print( "Results command executed successfully")
                return command
            except Exception as e:
                print( f"Error executing results command: {str(e)}")
        print ("Results command not executed successfully")        
    return None


def create_update_ranks_command():
    command = UpdateRanksCommand.UpdateRanksCommand()
    
    try:
        db.session.add(command)
        db.session.commit()
        return command
    except Exception as e:
        print(f"Error executing update ranks command: {str(e)}")
        return None
    
def execute_update_ranks_command(admin_id):
    
    admin = Admin.query.get(admin_id)
    
    if admin:
        command = create_update_ranks_command()
        if command:
            try:
                command.execute()
                print("Update ranks command executed successfully")
            except Exception as e:
                print(f"Error executing update ranks command: {str(e)}")
        else:
            print("Update ranks command not executed successfully")
    return None

def create_rank_command(competitor_id, old_rank, new_rank):
    command = RankCommand(competitor_id, old_rank, new_rank)
    
    try:
        db.session.add(command)
        db.session.commit()
        return command
    except Exception as e:
        print(f"Error executing rank command: {str(e)}")
        return None
    
def execute_rank_command(competitor_id, old_rank,  new_rank):
    
    admin = Admin.query.get(000)
    
    if admin is None:
        command = create_rank_command(competitor_id, old_rank, new_rank)
        if command:
            try:
                command.execute()
                print("Rank command executed successfully")
            except Exception as e:
                print(f"Error executing rank command: {str(e)}")
        else:
            print("Rank command not executed successfully")
    return None

def create_points_command(competitor_id):
    command = PointsCommand.PointsCommand(competitor_id)
    
    try:
        db.session.add(command)
        db.session.commit()
        return command
    except Exception as e:
        print(f"Error executing points command: {str(e)}")
        return None
    
def execute_points_command(admin_id, competitor_id):
    
    admin = Admin.query.get(admin_id)
    
    if admin:
        command = create_points_command(competitor_id)
        if command:
            try:
                command.execute()
                print("Points command executed successfully")
            except Exception as e:
                print(f"Error executing points command: {str(e)}")
        else:
            print("Points command not executed successfully")
    return None


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
