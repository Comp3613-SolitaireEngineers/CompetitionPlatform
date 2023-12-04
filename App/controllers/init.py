from App.database import db
from App.controllers import *
from App.models import *
from datetime import datetime, date
from App.controllers import create_admin, create_competition, create_competitor, execute_competition_command, create_host, create_competition_host, create_rank_top_observers

def initialize_db():

    rank_top_observer = create_rank_top_observers("Rank Top Observers")
    
    admin = create_admin(uwi_id='816012345', username='admin', email="bob.burgers@sta.uwi.edu", password="adminpass")
    competition1 = execute_competition_command(admin_id=admin.id,name='UWI Games 2020', date=date(2020, 2, 29), location='UWI SPEC', platform='HackerRank')
    competition2 = execute_competition_command(admin_id=admin.id,name='UWI Games 2021', date=date(2021, 2, 28), location='UWI SPEC', platform='HackerRank')
    competition3 = execute_competition_command(admin_id=admin.id,name='UWI Games 2022', date=date(2022, 2, 27), location='UWI SPEC', platform='HackerRank')
    competition4 = execute_competition_command(admin_id=admin.id,name='UWI Games 2023', date=date(2023, 2, 26), location='UWI SPEC', platform='HackerRank')
    competition5 = execute_competition_command(admin_id=admin.id,name='UWI Games 2024', date=date(2024, 2, 25), location='UWI SPEC', platform='HackerRank')

   
    competitor1 = create_competitor(uwi_id='816024682', firstname='Morty', lastname='Smith', username='king_morty', password='mortypass', email= 'morty.smith@my.uwi.edu')
    competitor2 = create_competitor(uwi_id='816024683', firstname='Rick', lastname='Sanchez', username='rickety_rick', password='rickypass', email= 'rick.sanchez@my.uwi.edi')
    competitor3 = create_competitor(uwi_id='816024684', firstname='Summer', lastname='Smith', username='summer_time', password='summerpass', email= 'summer.smith@my.uwi.edu')
    competitor4 = create_competitor(uwi_id='816024685', firstname='Beth', lastname='Smith', username='bethany', password='bethpass', email= 'beth.smith@my.uwi.edu')
    competitor5 = create_competitor(uwi_id='816024686', firstname='Jerry', lastname='Smith', username='jerry_berry', password='jerrypass', email= 'jerry.smith@my.uwi.edu')                            
    competitor6 = create_competitor(uwi_id='816024687', firstname='Bird', lastname='Person', username='birdperson', password='birdpass', email='bird.person@my.uwi.edu') 
    competitor7 = create_competitor(uwi_id='816024688', firstname='Squanchy', lastname='Smith', username='squanchy', password='squanchypass', email= 'squanchy.smith@my.uwi.edu') 
   

    host1 = create_host(name="CodeCrafters Club", website="www.codecraftersclub.com")
    host2 = create_host(name="UWICS Club", website="https://www.instagram.com/uwics_club/?hl=en")
    host3 = create_host(name="DCIT", website="https://sta.uwi.edu/fst/dcit/")

    comp_host1 = create_competition_host(comp_id=competition1.id, host_id = host1.id)
    comp_host1 = create_competition_host(comp_id=competition2.id, host_id = host1.id)
    comp_host1 = create_competition_host(comp_id=competition3.id, host_id = host2.id)
    comp_host1 = create_competition_host(comp_id=competition4.id, host_id = host3.id)
    comp_host1 = create_competition_host(comp_id=competition5.id, host_id = host3.id)

