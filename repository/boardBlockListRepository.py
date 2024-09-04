
from repository.repositoryConfig import client, RepositoryConfig
from model.boardBlockList import BoardBlockList
from datetime import datetime, timezone, timedelta
from pymongo import UpdateOne

class BoardBlockListRepository:

    COLLECTION_NAME = 'boardBlockList'
    
    def __init__(self, client):
        self.client = client
        self.db = client[RepositoryConfig.databaseName]
        self.collection = self.db[self.COLLECTION_NAME]

    def updateCount(self, newOpenList):
        self.collection.update_one(
            {'_id': newOpenList._id},
            {'$set': { newOpenList.to_dict() }},
            upsert=True
        )

    def todayOpenList(self):
        current = datetime.now(timezone(timedelta(hours=9-6)))
        year = current.year
        month = current.month
        day = current.day
        todayKey = f"{year}-{month}-{day}"

        for data in self.collection.find():
            item = BoardBlockList.from_dict(data)
            if item._id.startswith(todayKey):
                return item
        return None

        if operations:
            self.collection.bulk_write(operations)


    def delete(self, _id):
        self.collection.delete_one(
            { '_id': _id }
        )

boardBlockListRepository = BoardBlockListRepository(client=client)

