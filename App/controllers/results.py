from App.database import db
from App.models import Results, Competitor, Competition
from App.controllers import create_competitor
import csv

def create_result(competition_id, competitor_id, points, rank):    
    competition = Competition.query.filter_by(id=competition_id).first()
    if competition is None:
        return None
    competitor = Competitor.query.filter_by(id=competitor_id).first()
    if competitor is None:
        return None
    
    try:
        result = Results(competition_id, competitor_id, points, rank)
        db.session.add(result)
        db.session.commit()       
        return result
    except Exception as e:
        print("here", e)
        db.session.rollback()
    return None

def get_all_results():
    results = Results.query.all()
    if results is None:
        return None
    return results

def get_all_results_json():
    results = Results.query.all()
    if results is None:
        return None
    return [result.get_json() for result in results]

def get_results_by_competition_id(competition_id):
    competition_results = []
    results = Results.query.filter_by(competition_id=competition_id).all()

    if results is None:
        return None
    
    for result in results:
        competitor = Competitor.query.filter_by(id=result.competitor_id).first()
        competition_results.append({
            'competitor': competitor.get_json(),
            'rank': result.rank,
            'points': result.points
        })

    return competition_results


def add_results(competition_id, results_file):
    
    competition = Competition.query.filter_by(id=competition_id).first()
    if competition is None:
        return None 

    if competition.results_added == True:
        return None       

    with open(results_file, 'r', newline='') as f:
        reader = csv.DictReader(f)
                   
        for line in reader:
            student_id = line['student_id']
            firstname = line['firstname']
            lastname = line['lastname']
            email = line['email']
            points = line['points']
            rank = line['rank']            
            competitor = Competitor.query.filter_by(uwi_id=student_id).first()
            if competitor is None:
                username = firstname[0].lower() + lastname.lower()+student_id[-2:]
                password = firstname[0].lower() + lastname[0].lower()+ student_id[-4:]
                # print("Student 1:" + username + " "+ password)
                competitor = create_competitor(student_id, username, email, password, firstname, lastname,)
                if competitor is None:
                    print("Student not created")
                    continue
                    
            result = create_result(competition_id, competitor.id, points, rank)                   
    
    competition.results_added = True
    return True
 


    