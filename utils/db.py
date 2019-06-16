from motor import motor_asyncio as mongod
client = mongod.AsyncIOMotorClient('localhost', 27017)
db = client.oompa2

def getDB():
    return db