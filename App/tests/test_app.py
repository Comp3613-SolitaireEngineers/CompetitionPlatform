import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User
from App.controllers import *


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        pass
        # user = User("bob", "bobpass")
        # assert user.username == "bob"

    # # pure function no side effects or integrations called
    # def test_get_json(self):
    #     user = User("bob", "bobpass")
    #     user_json = user.get_json()
    #     self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    # def test_hashed_password(self):
    #     password = "mypass"
    #     hashed = generate_password_hash(password, method='sha256')
    #     user = User("bob", password)
    #     assert user.password != password

    # def test_check_password(self):
    #     password = "mypass"
    #     user = User("bob", password)
    #     assert user.check_password(password)

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


