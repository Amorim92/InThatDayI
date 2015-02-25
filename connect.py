import dropdb
import createdb

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

dropdb.dropDatabase(client)

db = createdb.createDatabase(client)


calendar = db.create_collection('calendar')
drive = db.create_collection('drive')
contacts = db.create_collection('contacts')
fitness = db.create_collection('fitness')
gmail = db.create_collection('gmail')
maps = db.create_collection('maps')
googleMore = db.create_collection('googleMore')
places = db.create_collection('places')

fitbit = db.create_collection('fitbit')
lastFm = db.create_collection('lastFm')
twitter = db.create_collection('twitter')
