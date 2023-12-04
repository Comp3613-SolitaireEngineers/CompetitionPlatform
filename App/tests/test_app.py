import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date

from App.main import create_app
from App.database import db, create_db
from App.controllers import *
#     create_competitor, 
#     get_competitor_profile, 
#     get_rankings, 
#     create_competition, 
#     get_competition_details, 
#     create_result,
#     get_all_competitions)
from App.models import Host, Admin, Competitor, Competition,Rank,Notification,Results,ResultsCommand,CompetitionCommand

LOGGER = logging.getLogger(__name__)
#test
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
        
    def test_new_admin(self):
        admin = Admin("817630671", "admin1", "sherry.floobs@mail.com", "admin1pass")
        assert admin.uwi_id == "817630671"
        assert admin.username == "admin1"
        assert admin.email == "sherry.floobs@mail.com"
        
    def test_new_competition(self):
        competition = Competition("UWI Games 2023", "DCIT Conference Room", "HankerRank", "01-02-2023")
        assert competition.name == "UWI Games 2023"
        assert competition.location == "DCIT Conference Room"
        assert competition.platform == "HankerRank"
        assert competition.date == "01-02-2023"

    # pure function no side effects or integrations called
    def test_competitor_get_json(self):
        competitor = Competitor("816011111", "coolGuy101", "randal.m@mail.com", "randalpass", "Randal", "Morris")
        competitor_json = competitor.get_json()

        self.assertDictEqual(
            competitor_json,
            {
                'id': competitor.id,
                'uwi_id': "816011111",
                'firstname': "Randal",
                'lastname': "Morris",
                'email': "randal.m@mail.com",
                'username': "coolGuy101",                
                'platform_rank':              
                        {   'id': 1,
                            'competitor_id': competitor.id,
                            'ranking': 1,                          
                            'points': 0,                        
                            'created_at': competitor.rank.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                            'updated_at': competitor.rank.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                        },                
                'role' : 'competitor'            
            })

    def test_host_get_json(self):
        host = Host("DCIT", "https://sta.uwi.edu/fst/dcit")
        host_json = host.toDict()
        
        self.assertDictEqual(
            host_json, 
            {
                "id": host.id, 
                "name": "DCIT",
                "website": "https://sta.uwi.edu/fst/dcit"
            })

    def test_admin_get_json(self):
        admin = Admin("817630671", "admin1", "sherry.floobs@mail.com", "admin1pass")
        admin_json = admin.get_json()

        self.assertDictEqual(
            admin_json,
            {
                'id': admin.id,
                'uwi_id': "817630671",
                'email': "sherry.floobs@mail.com",
                'username': "admin1",
                'role' : 'admin'
            })

    def test_competition_get_json(self):
        date = datetime.now()
        competition = Competition("UWI Games 2023", "DCIT Conference Room", "HankerRank", date)
        competition_json = competition.get_json()

        self.assertDictEqual(
            competition_json, 
            {
                'id': None,
                'name': "UWI Games 2023",
                'location': "DCIT Conference Room",
                'platform': "HankerRank",
                'date': date.strftime("%Y-%m-%d %H:%M:%S"),
                "hosts": [],
                "participants": []
            })
        
    def test_hashed_password(self):
        password = "password"
        hashed = generate_password_hash(password, method='scrypt')
        admin = Admin("817630671", "admin1", "sherry.floobs@mail.com", password)
        
        assert admin.password != password

    def test_check_password(self):
        password = "admin1pass"
        admin = Admin("817630671", "admin1", "sherry.floobs@mail.com", password)
        
        assert admin.check_password(password)
        
    def test_new_notifcation(self):
        notification = Notification("10","Congratulations","2023-01-20")
        assert notification.competitor_id == "10"
        assert notification.message == "Congratulations"
        assert notification.timestamp == "2023-01-20"
            
    def test_new_notifcation_get_json(self):
        date = datetime.now()
        notification = Notification("10","Congratulations",date)
        notification_json = notification.get_json()
        self.assertDictEqual(
            notification_json, 
            {
            'id':None, 
            'competitor_id':"10",
            'message':"Congratulations",
            'timestamp':date.strftime("%Y-%m-%d %H:%M:%S")
            })
        
    def test_new_rank(self):
        #rank = Rank("10","2023-02-05","2023-05-20")
        rank = Rank("10")
        assert rank.competitor_id == "10"
        #assert rank.created_at == "2023-02-05"
        #assert rank.updated_at == "2023-05-20"
        
    def test_new_rank_get_json(self):

        date = datetime.now()
        #rank = Rank("10",date,date)
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
                #'created_at':None,
                #'updated_at':None
            })
          
              
    def test_new_results(self):
        result = Results("123","12","10","1","2023-02-20","2023-05-20")
        assert result.competition_id == "123"
        assert result.competitor_id == "12"
        assert result.points == "10"
        assert result.rank == "1"
        assert result.date_created == "2023-02-20"
        assert result.date_modified == "2023-05-20"
        
    def test_new_results_get_json(self):
        date = datetime.now()
        result = Results("123","12","10","1",date,date)
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
        date = datetime.now()
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

    def test_veiw_competitions_success(self):
        competition1 = create_competition("UWI Games 2023", "DCIT Conference Room", "HackerRank", date(2023, 2, 26))
        competition2 = create_competition("UWI Games 2024", "DCIT Conference Room", "HackerRank", date(2024, 2, 25))

        competitions = get_all_competitions()
        assert len(competitions) == 2
        assert competitions[0].name == "UWI Games 2023"
        assert competitions[1].name == "UWI Games 2024"
    
    def test_view_competitions_fail(self):
        competition1 = create_competition("UWI Games 2023", "DCIT Conference Room", "HackerRank", date(2025, 2, 26))
        competition2 = create_competition("UWI Games 2024", "DCIT Conference Room", "HackerRank", date(2026, 2, 25))
        competition3 = create_competition("UWI Games 2024", "DCIT Conference Room", "HackerRank", date(2026, 2, 25))

        competitions = get_all_competitions()
        print(com.name for com in competitions)
        assert len(competitions) != 6
        assert competitions[2].name != "UWI Games 2025"
        assert competitions[3].name != "UWI Games 2026"


    def test_view_comoetition_details_success(self):
        competition = create_competition("UWI Games 2027", "DCIT Conference Room", "HackerRank", date(2027, 2, 26))
        competitor = create_competitor(uwi_id='816024687', firstname='Bird', lastname='Person', username='birdperson', password='birdpass', email='bird.person@my.uwi.edu')
        results = create_result(competition.id, competitor.id, 25, 3)
        competition_details = get_competition_details(competition.id)
        assert competition_details['name'] == "UWI Games 2027"
        assert competition_details['location'] == "DCIT Conference Room"
        assert competition_details['platform'] == "HackerRank"
        assert competition_details['date'] == "26 February, 2027"
        
        assert competition_details['results'][0]['competitor']['username'] == "birdperson"
        assert competition_details['results'][0]['competitor']['firstname'] == "Bird"
        assert competition_details['results'][0]['competitor']['lastname'] == "Person"
        assert competition_details['results'][0]['competitor']['email'] == "bird.person@my.uwi.edu"
        assert competition_details['results'][0]['competitor']['platform_rank']['ranking'] == 3
        assert competition_details['results'][0]['competitor']['platform_rank']['points'] == 0
        assert competition_details['results'][0]['rank'] == 3
        assert competition_details['results'][0]['points'] == 25

    def test_view_competition_details_failure(self):
       
        competition = create_competition("UWI Games 2028", "DCIT Conference Room", "HackerRank", date(2028, 2, 26))
        nonexistent_competition_id = 0
    
        competition_details = get_competition_details(nonexistent_competition_id)
        
        assert competition_details is None 

    def test_view_rankings_fail(self):
        competitor1 = create_competitor(uwi_id='816024687', firstname='Eren', lastname='Jaegar', username='killer', password='attack', email= 'eren.yaegar@my.uwi.edu')
        competition = create_competition("UWI Games 2029", "DCIT Conference Room", "HackerRank", date(2029, 2, 26))
        results = create_result(competition.id, "816024687", 25, 1)

        rankings = get_rankings()
        assert len(rankings) != 4       

    def test_view_rankings_success(self):
        competitor1 = create_competitor(uwi_id='816024685', firstname='Mikasa', lastname='Ackerman', username='mika', password='ackerman', email= 'mikasa.ackerman@my.uwi.edu')
        competition = create_competition("UWI Games 2030", "DCIT Conference Room", "HackerRank", date(2030, 2, 26))
        results = create_result(competition.id, competitor1.id, 25, 1)

        rankings = get_rankings()
        assert len(rankings) == 4
        assert rankings[3]["ranking"] == 4
        assert rankings[3]["competitor_id"] == competitor1.id 
        assert rankings[3]["name"] == "Mikasa Ackerman"

        









    # def test_get_rankings_fail(self):
    #     # competitor = create_competitor(uwi_id='816024683', firstname='Jerry', lastname='Sanchez', username='rickety_jerry', password='jerrypass', email= 'rick.sanchez@my.uwi.edi')
    #     rankings = get_rankings()
    #     assert len(rankings) != 4
    #     print(rankings)
    #     assert rankings[2]["ranking"] != 4
    #     assert rankings[2]["competitor_id"] != 0
    #     assert rankings[2]["name"] != "Jerry Sanchez"

    # def test_get_rankings_success(self):        
    #     competitor = create_competitor(uwi_id='816024684', firstname='Beth', lastname='Smith', username='betty', password='bettypass', email= 'betty.smith@my.uwi.edu')

    #     rankings = get_rankings()
    #     assert len(rankings) == 4
    #     assert rankings[3]["ranking"] == 3
    #     assert rankings[3]["competitor_id"] == competitor.id
    #     assert rankings[3]["name"] == "Beth Smith"

   

   
    

    

    def test_competition_creation(self):
        competition = create_competition("name", "locations", "platform", datetime.utcnow())
        assert competition.id is not None, "Failed to create competition"

    def test_competition_command(self):
        competition = create_competition("New Competition", "Italia", "Online", datetime.utcnow())
        self.assertIsNotNone(competition)
        self.assertEqual(competition.name, "New Competition")
        
    def test_results_command(self):
        
        # Create a competition_id and admin_id for testing
        admin = create_admin(113242,"emailaas","usernameaqeq","passwordqedqa")   
        self.assertIsNotNone(admin)
        
        competition = create_competition("nameedqd", "location", "online", datetime.utcnow())
        self.assertIsNotNone(competition)

        # Prepare some results for testing
        results = 'App/static/tests/results.csv'

        command = execute_results_command(admin.id, competition.id, results)
        self.assertIsNotNone(command)

        comp_results = get_results_by_competition_id(competition.id)
        
        self.assertEqual(len(comp_results), 5)

    def test_notify_subscribers(self):
        # Create a RankTopObservers instance
        observers = create_rank_top_observers("Top 20 Observers")
        self.assertIsNotNone(observers), "Failed to create RankTopObservers"

        # Create a competitor and subscribe
        competitor = create_competitor(133434, "user", "pass", "email ", "sara", "lara")
        observers.subscribe(competitor)

        # Test notify_subscribers
        observers.notify_subscribers()

        # Check if the notifications were created correctly
        notifications = Notification.query.all()
        self.assertEqual(len(notifications), 1), "Incorrect number of notifications"
        
        competitors = [create_competitor(id, f"user{id}", f"pass{id}", f"email{id}", f"f{id}", f"l{id}") for id in range(1334314, 1334341)]
        
        for i in competitors:
            observers.subscribe(i)
            
        # Test notify_subscribers
        observers.notify_subscribers()
        assert len(competitors) == 27, "Failed to create competitors"
        
        notifications = get_notifications()

        self.assertEqual(len(notifications), 21), "Incorrect number of notifications"








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


