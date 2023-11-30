from App.controllers.host import create_host, get_all_hosts_json
import click, pytest, sys
from App.controllers.admin import create_admin, get_all_admins_json, update_admin
from flask import Flask
from datetime import datetime

from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import *



# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    initialize_db()    
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
# @user_cli.command("create", help="Creates a user")
# @click.argument("username", default="rob")
# @click.argument("password", default="robpass")
# def create_user_command(username, password):
#     create_user(username, password)
#     print(f'{username} created!')

# this command will be : flask user create bob bobpass

# @user_cli.command("list", help="Lists users in the database")
# @click.argument("format", default="string")
# def list_user_command(format):
#     if format == 'string':
#         print(get_all_users())
#     else:
#         print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

# @test.command("competition", help = 'Testing Competition commands')
# @click.argument("type", default="all")
# def competition_tests_command(type):
#     if type == "unit":
#         sys.exit(pytest.main(["-k", "CompUnitTests"]))
#     elif type == "int":
#         sys.exit(pytest.main(["-k", "CompIntegrationTests"]))
#     else:
#         print("deafult input, no test ran")

app.cli.add_command(test)


'''
Competition Commands
'''

competition_cli = AppGroup('competition', help = 'Competition object commands')   

@competition_cli.command("create", help = 'Creates new competition')
@click.argument("name", default ="Run Time")
@click.argument("location", default ="Chaguanas")
@click.argument("platform", default ="HackerRank")
def create_competition_command(name,location,platform):
    competition_date = date(2020, 2, 29)
    competition = create_competition(name,location,platform,competition_date)
    if competition:
        print("Competition Created Successfully")
    else:
        print("Competition not created")

@competition_cli.command("get_competition", help = " get competition")
def get_competition_by_id_command(id):
    competition = get_competition_by_id(id)
    if competition :
        print(competition)
    else: 
        print("No competition Found")


@competition_cli.command("list", help = "Lists all competitions")
def list_competitions_command():
    competitions = get_all_competitions_json()
    print(competitions)

app.cli.add_command(competition_cli)


'''
Competitor commands
'''

competitor = AppGroup('competitor', help = 'commands for competitor')

@competitor.command("create", help = 'create new competitor')
@click.argument("username", default = "rick")
@click.argument("email", default = "rick.sanchez@my.uwi.edu")
@click.argument("password", default = "sanchez")
@click.argument("uwi_id", default = "123456789")
@click.argument("firstname", default = "rick")
@click.argument("lastname", default = "sanchez")
def create_competitor_command( uwi_id, username, email,password, firstname, lastname):
    competitor = create_competitor(uwi_id, username,email, password, firstname, lastname)
    if competitor:
        print("Competitor Created Successfully ", competitor.get_json())
    else:
        print("Error adding competitor")

@competitor.command("list", help = 'list all competitors')
def list_competitors_command():
    competitors = get_all_competitors()
    if competitors:
        for competitor in competitors:
            print(competitor)
    else:
        print("Error getting competitors")

@competitor.command("get_competitor", help = 'get competitor by id')
def get_competitor_command():
    id  = click.prompt("Enter id", type=str)
    competitor = get_competitor_by_id(id)
    if competitor:
        print(competitor)
    else:
        print("Error getting competitor")

@competitor.command("get_competitor_json", help = 'get competitor by id')
def get_competitor_json_command():
    id = click.prompt("Enter id", type=str)
    competitor = get_competitor_by_id(id)
    if competitor:
        print(competitor.get_json())
    else:
        print("Error getting competitor")

@competitor.command("get_competitor_by_username", help = 'get competitor by username')
def get_competitor_by_username_command():
    username = click.prompt("Enter username", type=str)
    competitor = get_competitor_by_username(username)
    if competitor:
        print(competitor)
    else:
        print("Error getting competitor")

app.cli.add_command(competitor)

'''
Rank commands
''' 

rank = AppGroup('rank', help = 'commands for rank')

@rank.command("create", help = 'create new rank')
def create_rank_command():
    competitor_id = click.prompt("Enter Competitor ID")    
    rank = create_rank(competitor_id)
    if rank:
        print("Rank Created Successfully")
    else:
        print("Error adding rank")

@rank.command("update_rank", help = 'update rank')
def update_rank_command():
    competitor_id = click.prompt("Enter Competitor ID")
    ranking = click.prompt("Enter Ranking", type = int)
    rank = update_rank(competitor_id, ranking)
    if rank:
        print("Rank Updated Successfully")
    else:
        print("Error updating rank")

@rank.command("update_points", help = 'update points')
def update_rank_points_command():
    competitor_id = click.prompt("Enter Competitor ID")
    points = click.prompt("Enter Points", type = int)
    rank = update_rank_points(competitor_id, points)
    if rank:
        print("Rank Updated Successfully")
    else:
        print("Error updating points")


@rank.command("list", help = 'list all ranks')
def list_ranks_command():
    ranks = get_all_ranks_json()
    if ranks:
        print(ranks)
    else:
        print("Error getting ranks")
    
@rank.command("get_rank_by_competitor_id", help = 'get rank by competitor id')
def get_rank_command():
    competitor_id = click.prompt("Enter Competitor ID")
    rank = get_rank_by_competitor_id(competitor_id)
    if rank:
        print(rank)
    else:
        print("Error getting rank")


app.cli.add_command(rank)


'''
Host Commands
''' 

host_cli = AppGroup('host', help = 'host object commands')

@host_cli.command('create', help='Creates a host')
@click.argument("id", default="1")
@click.argument("name", default="bob")
@click.argument("website", default="hostwebsite@gmail.com")
def create_admin_command(id, name, website):
    host = create_host(id, name, website)
    if host:
        print(f'{name} created!')
    else:
        print(f'{name} not created')
        
@host_cli.command("list", help="Lists hosts in the database")
def list_host_command():
    hosts = get_all_hosts_json()
    if hosts:
        print(hosts)
    else:
        print("No Hosts Founds")
    
app.cli.add_command(host_cli)

'''
Admin Commands
'''

admin_cli = AppGroup('admin', help='Admin object commands')

@admin_cli.command("create", help="Creates an admin")
@click.argument("uwi_id", default="816099123")
@click.argument("email", default="admin@sta.uwi.edu")
@click.argument("username", default="bob")
@click.argument("password", default="bobpass")


def create_admin_command(uwi_id,username,email,password):
    admin = create_admin(uwi_id,username, email, password)
    if admin:
        print(f'{username} created!')
    else:
        print(f'{username} not created')

@admin_cli.command("list", help="Lists admins in the database")
def list_admin_command():
    admins = get_all_admins_json()    
    if admins:
        print(admins)
    else:
        print("No Admins Founds")
    
@admin_cli.command("update",help = "Updates an admin in the database")
@click.argument("id", default="std1")
@click.argument("username", default="bob")
def update_admin_command(id,username):
    admin = update_admin(id,username)
    if admin:
        print(f'Admin {id} updated!')
    else:
        print(f'{id} not updated!')

app.cli.add_command(admin_cli) 


'''
Results commands
'''

results = AppGroup('results', help = 'commands for results')

@results.command("create", help = 'create new result')
def create_result_command():
    competition_id = click.prompt("Enter Competition ID")
    competitor_id = click.prompt("Enter Competitor ID")
    points = click.prompt("Enter Points")
    rank = click.prompt("Enter Rank")
    result = create_result(competition_id, competitor_id, points, rank)
    if result:
        print("Result Created Successfully")
    else:
        print("Error adding result")

@results.command("list", help = 'list all results')
def list_results_command():
    results = get_all_results_json()
    if results:
        print(results)
    else:
        print("Error getting results")

@results.command("get_competition_results", help = 'get result by id')
def get_competition_results_command():
    competition_id = click.prompt("Enter Competition ID")
    results = get_results_by_competition_id(competition_id)
    if results:
        print(results)
    else:
        print("Error getting results")

@results.command("add", help = 'add results to competition')
def add_results_command():
    competition_id = click.prompt("Enter Competition ID")
    results_file = 'App/static/results.csv'
    response = add_results(competition_id,results_file)
    if response:
        print("Results Added Successfully")
    else:
        print("Error adding results")

app.cli.add_command(results)
