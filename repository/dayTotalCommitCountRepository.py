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

    def todayCumulative(self):
        # 오늘의 누적값 넣어줄 때 이전 날꺼 누적값을 반환
        currentDay = datetime.now(timezone(timedelta(hours=9-6))) 
        key = self.makeKey(currentDay)
        for data in self.collection.find():
            if data.get('_id') == key:
                return data.get('cumulativeCount')
        return 0

    def lastDayCumulative(self):
        # 오늘의 누적값 넣어줄 때 이전 날꺼 누적값을 반환
        lastDay = datetime.now(timezone(timedelta(hours=9-6-24))) 
        key = self.makeKey(lastDay)
        for data in self.collection.find():
            if data.get('_id') == key:
                return data.get('cumulativeCount')
        return 0

    def makeKey(self, daytime):
        year = daytime.year
        month = daytime.month
        day = daytime.day
        return f"{year}-{month}-{day}"

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