from repository.repositoryConfig import client, RepositoryConfig
from datetime import datetime, timezone, timedelta
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

    def todayCount(self):
        current = datetime.now(timezone(timedelta(hours=9-6)))
        year = current.year
        month = current.month
        day = current.day
        key = f"{year}-{month}-{day}"

        list = []
        for data in self.collection.find():
            item = DayTotalCommitCount.from_dict(data)
            if item._id == key:
                list.append(item)

        totalCommitCount = sum([ item.count for item in list])
        return totalCommitCount;

    def update(self, newModel):
        self.collection.update_one(
            {'_id': newModel._id},
            {'$set': newModel.to_dict() },
            upsert=True
        )

    def delete(self, _id):
        self.collection.delete_one(
            { '_id': _id }
        )

dayTotalCommitCountRepository = DayTotalCommitCountRepository(client)