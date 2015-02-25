from pymongo import MongoClient

def createDatabase(client) :
    print 'Create db InThatDayI'
    return client['InThatDayI']