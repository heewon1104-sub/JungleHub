from repository.repositoryConfig import client
from datetime import datetime, timezone
from model.dayTotalCommitCount import DayTotalCommitCount

class DayTotalCommitCountRepository: 

    def __init__(self, client):
        self.client = client
        self.db = client['dbjungle']
        self.collection = self.db['dayTotalCount']

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
    
    def updateCount(self, dayTotalCount, newCount):
        self.collection.update_one(
            {'key': dayTotalCount.key},
            {'$set': { 'count': newCount, 'updatedAt': datetime.now(timezone.utc) }}
        )

    def delete(self, key):
        self.collection.delete_one(
            { 'key': key }
        )

dayTotalCommitCountRepository = DayTotalCommitCountRepository(client)