from pymongo import MongoClient


def connection():
    # Mongo client
    client = MongoClient('localhost', 27017)

    # Drop database
    client.drop_database('InThatDayI')

    # Create new database
    db = client['InThatDayI']

    # Collections creation
    totalCount = db.create_collection('counters')
    terms_day = db.create_collection('terms_day')
    terms_week = db.create_collection('terms_week')
    terms_month = db.create_collection('terms_month')
    terms_year = db.create_collection('terms_year')
    people = db.create_collection('people')
    dates = db.create_collection('dates')


    return totalCount, terms_day, terms_week, terms_month, terms_year, people, dates