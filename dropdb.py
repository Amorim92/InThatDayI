from pymongo import MongoClient

def dropDatabase(client) :

    dbNames = client.database_names()

    for name in dbNames:
        client.drop_database(name)
        print 'Drop database ' + name
