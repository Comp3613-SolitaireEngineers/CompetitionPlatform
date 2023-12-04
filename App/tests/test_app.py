import pytest, logging, unittest
from werkzeug.security import generate_password_hash
from datetime import datetime, date

from App.main import create_app
from App.database import db, create_db
from App.controllers import *
from App.models import Host, Admin, Competitor, Competition,Rank,Notification,Results,ResultsCommand,CompetitionCommand

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
                        {   'id': None,
                            'competitor_id': None,
                            'ranking': 1,                          
                            'points': None,                        
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
        hashed = generate_password_hash(password, method='sha256')
        admin = Admin("817630671", "admin1", "sherry.floobs@mail.com", password)
        
        assert admin.password != password

    def test_check_password(self):
        password = "admin1pass"
        admin = Admin("817630671", "admin1", "sherry.floobs@mail.com", password)
        
        assert admin.check_password(password)
        
    def test_new_notifcation(self):
        notification = Notification("10","Congratulations","Title")
        assert notification.competitor_id == "10"
        assert notification.message == "Congratulations"
        assert notification.title == "Title"
        assert notification.timestamp.strftime('%Y-%m-%d') == datetime.now().strftime('%Y-%m-%d')

            
    def test_new_notifcation_get_json(self):
        date = datetime.now()
        notification = Notification("10","Congratulations","Title")
        notification_json = notification.get_json()
        self.assertDictEqual(
            {key: value for key, value in notification_json.items() if key != 'timestamp'},
            {
            'id':None, 
            'competitor_id':"10",
            'message':"Congratulations",
            "title" : "Title"
            })
        notification_date = datetime.strptime(notification_json['timestamp'], "%Y-%m-%d %H:%M:%S").date()
        self.assertEqual(notification_date, date.date())

        
    def test_new_rank(self):
        rank = Rank("10")
        assert rank.competitor_id == "10"
        
    def test_new_rank_get_json(self):

        date = datetime.now()
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
     
    def test_new_competition_command(self):
        competition = Competition("UWI Games 2023", "DCIT Conference Room", "HankerRank", "01-02-2023")
        compCmd = CompetitionCommand()
        compCmd.set_competition_id(competition.id)
        assert compCmd is not None
        assert compCmd.competition_id == competition.id
        assert compCmd.executed_at is not None
    
    def test_new_competition_command_get_json(self):
        competition = Competition("UWI Games 2024", "DCIT Conference Room", "HankerRank", "01-02-2023")
        compCmd = CompetitionCommand()
        compCmd.set_competition_id(competition.id)
      
        compCmd_json = compCmd.get_json()
        self.assertDictEqual(
             compCmd_json,
             {
                 'id':2,
                 'competition_id': None,
                 'executed_at': compCmd.executed_at.strftime("%Y-%m-%d %H:%M:%S")
             })     
              
    def test_new_results(self):
        result = Results("123","12",10,1)
        assert result.competition_id == "123"
        assert result.competitor_id == "12"
        assert result.points == 10
        assert result.rank == 1
    
    def test_new_results_get_json(self):
        date = datetime.now()
        result = Results("123","123",100,11)
        assert result is not None
        result_json = result.get_json()
        expected_dict = {
            'id':None,
            'competition_id':"123",
            'competitor_id':"123",
            'rank':11,
            'points':100,
        }
        self.assertDictEqual(
            {key: result_json[key] for key in expected_dict.keys()},
            expected_dict
        )
        
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
    user = create_admin("1357924681","email1@example.com","admin1234","adminpass")
    assert login("email1@example.com", "adminpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
        self.client = self.app.test_client()
        create_db()
        yield self.app.test_client()
        db.drop_all()

    def test_1_get_competitor_profile_success(self):
        competitor = create_competitor(uwi_id='816024682', firstname='Morty', lastname='Smith', username='king_morty', password='mortypass', email= 'morty.smith@my.uwi.edu')       
        competitor_profile = get_competitor_profile(competitor.id)
        assert competitor_profile["username"] == "king_morty"
        assert competitor_profile["name"] == "Morty Smith"
        assert competitor_profile["email"] == "morty.smith@my.uwi.edu"

    def test_2_get_competitor_profile_fail(self):
        competitor = create_competitor(uwi_id='816024683', firstname='Rick', lastname='Sanchez', username='rickety_rick', password='rickypass', email= 'rick.sanchez@my.uwi.edi')
        competitor_profile = get_competitor_profile(0)
        assert competitor_profile == None

    def test_3_veiw_competitions_success(self):
        admin = create_admin("123456781","emailaas1","usernameaqeq1","passwordqedqa")
        competition1 = execute_competition_command(admin.id,"UWI Games 2023", "DCIT Conference Room", "HackerRank", date(2023, 2, 26))
        competition2 = execute_competition_command(admin.id,"UWI Games 2024", "DCIT Conference Room", "HackerRank", date(2024, 2, 25))

        competitions = get_all_competitions()
        assert len(competitions) == 2
        assert competitions[0].name == "UWI Games 2023"
        assert competitions[1].name == "UWI Games 2024"
    
    def test_4_view_competitions_fail(self):
        admin = create_admin("123456782","emailaas2","usernameaqeq2","passwordqedqa")
        competition1 = execute_competition_command(admin.id,"UWI Games 2023", "DCIT Conference Room", "HackerRank", date(2025, 2, 26))
        competition2 = execute_competition_command(admin.id,"UWI Games 2024", "DCIT Conference Room", "HackerRank", date(2026, 2, 25))
        
        competitions = get_all_competitions()        
        assert len(competitions) != 4

    def test_5_view_competition_details_success(self):
        admin = create_admin("123456783","emailaas3","usernameaqeq3","passwordqedqa")
        competition = execute_competition_command(admin.id,"UWI Games 2027", "DCIT Conference Room", "HackerRank", date(2027, 2, 26))
        competitor = create_competitor(uwi_id='816024687', firstname='Bird', lastname='Person', username='birdperson', password='birdpass', email='bird.person@my.uwi.edu')
        results = create_result(competition.id, competitor.id, 100, 1)
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
        assert competition_details['results'][0]['rank'] == 1
        assert competition_details['results'][0]['points'] == 100

    def test_6_view_competition_details_failure(self):        
        nonexistent_competition_id = "Nonexistent Competition ID"   
        competition_details = get_competition_details(nonexistent_competition_id)        
        assert competition_details is None 
        

    def test_7_view_rankings_success(self):
        admin = create_admin("123456784","emailaas4","usernameaqeq4","passwordqedqa")
        competitor1 = create_competitor(uwi_id='816024685', firstname='Mikasa', lastname='Ackerman', username='mika', password='ackerman', email= 'mikasa.ackerman@my.uwi.edu')
        competition = execute_competition_command(admin.id,"UWI Games 2030", "DCIT Conference Room", "HackerRank", date(2030, 2, 26))
        results = create_result(competition.id, competitor1.id, 85, 2)

        rankings = get_rankings()
        print(rankings)
        assert len(rankings) == 4
        assert rankings[3]["ranking"] == 4
        assert rankings[3]["competitor_id"] == competitor1.id 
        assert rankings[3]["name"] == "Mikasa Ackerman"

    def test_8_view_rankings_fail(self):
        admin = create_admin("123456785","emailaas5","usernameaqeq5","passwordqedqa")
        competitor1 = create_competitor(uwi_id='816024686', firstname='Eren', lastname='Jaegar', username='killer', password='attack', email= 'eren.yaegar@my.uwi.edu')
        competition = execute_competition_command(admin.id,"UWI Games 2029", "DCIT Conference Room", "HackerRank", date(2029, 2, 26))
        results = create_result(competition.id, "816024685", 55, 3)

        rankings = get_rankings()
        assert len(rankings) != 6
        assert rankings[4]["ranking"] != 4 
        assert rankings[3]["competitor_id"] != competitor1.id
        assert rankings[4]["name"] != "Mika Ackerman"


    def test_90_competition_creation(self):
        admin = create_admin("123456789","emailaas6","usernameaqeq6","passwordqedqa")
        competition = create_competition(admin.id, "name", "locations", "platform", datetime.now())
        assert competition.id is not None, "Failed to create competition"

    def test_91_competition_command(self):
        admin = create_admin("123456786","emailaas7","usernameaqeq7","passwordqedqa")
        competition = execute_competition_command(admin.id,"New Competition", "Italia", "Online", datetime.now())
        self.assertIsNotNone(competition)
        self.assertEqual(competition.name, "New Competition")
        
    def test_92_results_command(self):
        
        # Create a competition_id and admin_id for testing
        admin = create_admin("123456780","emailaas8","usernameaqeq8","passwordqedqa")   
        self.assertIsNotNone(admin)
        
        competition = execute_competition_command(admin.id,"nameedqd", "location", "online", datetime.now())
        self.assertIsNotNone(competition)

        # Prepare some results for testing
        results = 'App/static/tests/results.csv'

        command = execute_results_command(admin.id, competition.id, results)
        self.assertIsNotNone(command)

        comp_results = get_results_by_competition_id(competition.id)
        
        self.assertEqual(len(comp_results), 5)
    
            
    def test_93_notify_subscribers(self):
        # Create a RankTopObservers instance
        observers = create_rank_top_observers("Top 20 Observers")
        self.assertIsNotNone(observers), "Failed to create RankTopObservers"

        # Create a competitor and subscribe
        competitor = create_competitor(133434, "user", "pass", "email ", "sara", "lara")
        observers.subscribe(competitor)

        # Test notify_subscribers
        observers.notify_subscribers()

        # Check if the notifications were created correctly
        notifications = get_notifications()
        self.assertEqual(len(notifications), 21), "Incorrect number of notifications"
        
        competitors = [create_competitor(id, f"user{id}", f"pass{id}", f"email{id}", f"f{id}", f"l{id}") for id in range(1334314, 1334341)]
        
        for i in competitors:
            observers.subscribe(i)
            
        # Test notify_subscribers
        observers.notify_subscribers()
        assert len(competitors) == 27, "Failed to create competitors"
        
        notifications = get_notifications()

        self.assertEqual(len(notifications), 41), "Incorrect number of notifications"
