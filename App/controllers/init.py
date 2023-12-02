from App.database import db
from App.controllers import *
from App.models import *
from datetime import datetime, date


def initialize_db():

    admin = create_admin(uwi_id='816012345', username='admin', email="bob.burgers@sta.uwi.edu", password="adminpass")
    competition1 = create_competition(name='UWI Games 2020', date=date(2020, 2, 29), location='UWI SPEC', platform='HackerRank')# description='The UWI Games is an annual event that brings together students from all campuses to compete in a variety of sports.')
    competition2 = create_competition(name='UWI Games 2021', date=date(2021, 2, 28), location='UWI SPEC', platform='HackerRank')# description='The UWI Games is an annual event that brings together students from all campuses to compete in a variety of sports.')
    competition3 = create_competition(name='UWI Games 2022', date=date(2022, 2, 27), location='UWI SPEC', platform='HackerRank')# description='The UWI Games is an annual event that brings together students from all campuses to compete in a variety of sports.')
    competition4 = create_competition(name='UWI Games 2023', date=date(2023, 2, 26), location='UWI SPEC', platform='HackerRank')# description='The UWI Games is an annual event that brings together students from all campuses to compete in a variety of sports.')
    competition5 = create_competition(name='UWI Games 2024', date=date(2024, 2, 25), location='UWI SPEC', platform='HackerRank')# description='The UWI Games is an annual event that brings together students from all campuses to compete in a variety of sports.')
    competitor1 = create_competitor(uwi_id='816024682', firstname='Morty', lastname='Smith', username='king_morty', password='mortypass', email= 'morty.smith@my.uwi.edu')

    competitor2 = create_competitor(uwi_id='816024683', firstname='Rick', lastname='Sanchez', username='rickety_rick', password='rickypass', email= 'rick.sanchez@my.uwi.edi')

    competitor3 = create_competitor(uwi_id='816024684', firstname='Summer', lastname='Smith', username='summer_time', password='summerpass', email= 'summer.smith@my.uwi.edu')

    competitor4 = create_competitor(uwi_id='816024685', firstname='Beth', lastname='Smith', username='bethany', password='bethpass', email= 'beth.smith@my.uwi.edu')

    competitor5 = create_competitor(uwi_id='816024686', firstname='Jerry', lastname='Smith', username='jerry_berry', password='jerrypass', email= 'jerry.smith@my.uwi.edu')
                                    
    competitor6 = create_competitor(uwi_id='816024687', firstname='Bird', lastname='Person', username='birdperson', password='birdpass', email='bird.person@my.uwi.edu') 

    competitor7 = create_competitor(uwi_id='816024688', firstname='Squanchy', lastname='Smith', username='squanchy', password='squanchypass', email= 'squanchy.smith@my.uwi.edu')                        


    # add_results(competition1.id, 'App/static/results.csv')
