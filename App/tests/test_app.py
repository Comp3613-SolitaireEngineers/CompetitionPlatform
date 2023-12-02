from datetime import date
import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import Host, Admin, Competitor, Competition, Notification, Rank, Results,ResultsCommand, CompetitionCommand
# from App.controllers import (
    # create_user,
    # get_all_users_json,
    # login,
    # get_user,
    # get_user_by_username,
    # update_user,
    # get_user_competitions,
    # create_competition,
    # add_user_to_comp,
    # get_user_rankings
# )

LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):
    def test_new_competitor(self):
        competitor = Competitor("816011111", "coolGuy101", "randal.m@mail.com", "randalpass", "Randal", "Morris")
        assert competitor.uwi_id == "816011111"
        assert competitor.username == "coolGuy101"
        assert competitor.email == "randal.m@mail.com"
        assert competitor.firstname == "Randal"
        assert competitor.lastname == "Morris"

    def test_new_host(self):
        host = Host("DCIT", "https://sta.uwi.edu/fst/dcit")
        assert host.name == "DCIT"
        assert host.website == "https://sta.uwi.edu/fst/dcit"
    
    def test_new_notifcation(self):
        notification = Notification("10","Congratulations")
        assert notification.competitor_id == "10"
        assert notification.message == "Congratulations"
            
    def test_new_notifcation_get_json(self):
        notification = Notification("10","Congratulations")
        notification_json = notification.toDict()
        self.assertDictEqual(
            notification_json, 
            {
            'id':None, 
            'competitor_id':"10",
            'message':"Congratulations",
            'timestamp':date.strftime("%Y-%m-%d %H:%M:%S")
            })
        
    def test_new_rank(self):
        rank = Rank("10")
        assert rank.competitor_id == "10"
        
    def test_new_rank_get_json(self):
        rank = Rank("10")
        rank_json = rank.get_json()
        self.assertDictEqual(
            rank_json,
            {
                'id':None,
                'competitor_id':"10",
                'ranking':1,
                'points':None,
                'created_at':date.strftime("%Y-%m-%d %H:%M:%S"),
                'updated_at':date.strftime("%Y-%m-%d %H:%M:%S")
            })
              
    def test_new_results(self):
        result = Results("123","12","10","1")
        assert result.competition_id == "123"
        assert result.competitor_id == "12"
        assert result.points == "10"
        assert result.rank == "1"
        
    def test_new_results_get_json(self):
        result = Results("123","12","10","1")
        result_json = result.get_json()
        self.assertDictEqual(
            result_json,
            {
                'id':None,
                'competition_id':"123",
                'competitor_id':"12",
                'rank':"1",
                'points':"10",
                'date_created':date.strftime("%Y-%m-%d %H:%M:%S"),
                'date_modified':date.strftime("%Y-%m-%d %H:%M:%S")
            })
        
    def test_new_results_command(self):
        reCmd = ResultsCommand("10")
        assert reCmd.competition_id == "10"
        
    def test_new_results_command_get_json(self):
        reCmd = ResultsCommand("10")
        reCmd_json = reCmd.get_json()
        self.assertDictEqual(
            reCmd_json,
            {
                'id':None,
                'competition_id':"10"
            })
             
    def test_new_competition_command(self):
        compCmd = CompetitionCommand("10")
        assert compCmd.competition_id == "10"
    
    def test_new_competition_command_get_json(self):
        compCmd = CompetitionCommand("10")
        compCmd_json = compCmd.get_json()
        self.assertDictEqual(
            compCmd_json,
            {
                'id':None,
                'competition_id':"10",
                'executed_at':date.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        
        
'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    pass
    # user = create_user("bob", "bobpass")
    # assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_get_competitor_profile_success(self):
        competitor = create_competitor(uwi_id='816024682', firstname='Morty', lastname='Smith', username='king_morty', password='mortypass', email= 'morty.smith@my.uwi.edu')       
        competitor_profile = get_competitor_profile(competitor.id)
        assert competitor_profile["username"] == "king_morty"
        assert competitor_profile["name"] == "Morty Smith"
        assert competitor_profile["email"] == "morty.smith@my.uwi.edu"

    def test_get_competitor_profile_fail(self):
        competitor = create_competitor(uwi_id='816024683', firstname='Rick', lastname='Sanchez', username='rickety_rick', password='rickypass', email= 'rick.sanchez@my.uwi.edi')
        competitor_profile = get_competitor_profile(0)
        assert competitor_profile == None

    def test_get_rankings(self):        
        competitor = create_competitor(uwi_id='816024684', firstname='Rick', lastname='Sanchez', username='rickety_rick1', password='rickypass', email= 'rick.sanchez1@my.uwi.edi')

        rankings = get_rankings()
        assert len(rankings) == 3
        assert rankings[0]["ranking"] == 1
        assert rankings[0]["competitor_id"] == competitor.id
        assert rankings[0]["name"] == "Rick Sanchez"










    # def test_create_user(self):
    #     user = create_user("rick", "bobpass")
    #     assert user.username == "rick"

    # def test_get_all_users_json(self):
    #     users_json = get_all_users_json()
    #     self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # # Tests data changes in the database
    # def test_update_user(self):
    #     update_user(1, "ronnie")
    #     user = get_user(1)
    #     assert user.username == "ronnie"

    # def test_add_user_to_comp(self):
    #     newcomp = create_competition("Walktime", "Port of Spain")
    #     if newcomp:
    #         assert add_user_to_comp(1, 1, 4)
    #     else:
    #         assert False

    # def test_get_user_competitions(self):
    #     comp = get_user_competitions(1)
    #     user_competitions = []

    #     for usercomp in comp:
    #         del usercomp["date"]
    #         del usercomp["hosts"]
    #         del usercomp["participants"]
    #         user_competitions.append(usercomp)
        
    #     expected_list = [{"id": 1, "name": "Walktime", "location": "Port of Spain"}]
    #     self.assertListEqual(expected_list, user_competitions)


    # def test_get_user_rankings(self):
    #     users = get_user_rankings(1)
        
    #     self.assertListEqual([{"id":1, "comp_id": 1 , "user_id": 1, "rank": 4}], users)


