# import os, tempfile, pytest, logging, unittest
# from werkzeug.security import check_password_hash, generate_password_hash

# from App.main import create_app
# from App.database import db, create_db
# from App.models import User, Competition
# from App.controllers import (
#     create_user,
#     get_all_users_json,
#     login,
#     get_user,
#     get_user_by_username,
#     update_user,

#     create_competition,
#     get_all_competitions,
#     get_all_competitions_json,
#     get_competition_by_id,

#     add_results,
#     get_competition_users


# )


# LOGGER = logging.getLogger(__name__)



# '''
#    Unit Tests
# '''

# class CompUnitTests(unittest.TestCase):

#     def test_new_comp(self):
#         testComp = Competition("Walktime", "Port of Spain")
#         assert testComp.name == "Walktime"


#     def test_comp_json(self):
#         testComp = Competition("Walktime", "Port of Spain")
#         testComp_json = testComp.get_json()
#         self.assertDictEqual(testComp_json, {"id":None, "name":"Walktime", "location": "Port of Spain"})


# # class CompIntegrationTests()

# #     # def test_new_user(self):
# #     #     user = User("bob", "bobpass")
# #     #     assert user.username == "bob"




# @pytest.fixture(autouse=True, scope="module")
# def empty_db():
#     app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
#     create_db()
#     yield app.test_client()
#     db.drop_all()


# def test_authenticate():
#     user = create_user("bob", "bobpass")
#     assert login("bob", "bobpass") != None



# class CompIntegrationTests(unittest.TestCase):

#     def test_create_competition(self):
#         assert create_competition("Walktime", "Port of Spain")


#     def test_get_comp_list(self):
#         competitions = get_all_competitions_json()
#         cleaned_competitions = []

#         for competitions_json in competitions:
#             del competitions_json["date"]
#             del competitions_json["hosts"]
#             del competitions_json["participants"]
#             cleaned_competitions.append(competitions_json)
        
#         expected_list = [{"id": 1, "name": "Walktime", "location": "Port of Spain"}]
#         self.assertListEqual(expected_list, cleaned_competitions)


#     def test_get_competition_by_id(self):
#         Competition_json = get_competition_by_id(1).get_json()
#         self.assertDictEqual(Competition_json, {"id":1, "name":"Walktime", "location": "Port of Spain"})
        


