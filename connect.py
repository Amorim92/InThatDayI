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
    pcUser = db.create_collection('user')

    # Collections to Google APIs
    calendar = db.create_collection('calendar')
    drive = db.create_collection('drive')
    gmail = db.create_collection('gmail')
    plus = db.create_collection('plus')

    lastFm = db.create_collection('lastFm')
    twitter = db.create_collection('twitter')
    facebook = db.create_collection('facebook')

    return totalCount, pcUser, calendar, drive, gmail, plus, lastFm, twitter, facebook