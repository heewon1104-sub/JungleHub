from repository.repositoryConfig import client, RepositoryConfig
from datetime import datetime, timezone
from model.dayTotalCommitCount import DayTotalCommitCount

class DayTotalCommitCountRepository: 

    COLLECTION_NAME = 'dayTotalCount'

    def __init__(self, client):
        self.client = client
        self.db = client[RepositoryConfig.databaseName]
        self.collection = self.db[self.COLLECTION_NAME]

    def create(self, dayTotalCount):
        data = dayTotalCount.to_dict()
        result = self.collection.insert_one(data)
        return dayTotalCount
    
    def readAll(self):
        list = []
        for data in self.collection.find():
            item = DayTotalCommitCount.from_dict(data)
            list.append(item)
        return list;
    
    def updateCount(self, _id, newCount):
        self.collection.update_one(
            {'_id': _id},
            {'$set': { 'count': newCount, 'updatedAt': datetime.now(timezone.utc) }}
        )

    def delete(self, _id):
        self.collection.delete_one(
            { '_id': _id }
        )

dayTotalCommitCountRepository = DayTotalCommitCountRepository(client)