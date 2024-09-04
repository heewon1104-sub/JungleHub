from repository.repositoryConfig import client, RepositoryConfig
from model.userCommitCount import UserCommitCount
from datetime import datetime, timezone, timedelta
from pymongo import UpdateOne

class UserCommitCountRepository:

    COLLECTION_NAME = 'userCommitCount'
    
    def __init__(self, client):
        self.client = client
        self.db = client[RepositoryConfig.databaseName]
        self.collection = self.db[self.COLLECTION_NAME]

    def create(self, userCommitCount):
        data = userCommitCount.to_dict()
        result = self.collection.insert_one(data)
        return userCommitCount
    
    def readAll(self):
        list = []
        for data in self.collection.find():
            item = UserCommitCount.from_dict(data)
            list.append(item)
        return list;

    def todayList(self):
        current = datetime.now(timezone(timedelta(hours=9-6)))
        year = current.year
        month = current.month
        day = current.day
        todayKey = f"{year}-{month}-{day}"

        list = []
        for data in self.collection.find():
            item = UserCommitCount.from_dict(data)
            if item._id.startswith(todayKey):
                list.append(item)
        return list
    
    def updateCount(self, userCommitCount, newCount):
        self.collection.update_one(
            {'_id': userCommitCount._id},
            {'$set': { 'count': newCount, 'updatedAt': datetime.now(timezone.utc) }}
        )

    # 될듯? 
    def updateAllUserCount(self, userIdAndNewCountList):
        
        list = []
        for data in userIdAndNewCountList: 
            model = UserCommitCount(
                _id = UserCommitCount.makeCurrentDayUserKey(data['userId']),
                userKey=data['userId'],
                count=data['totalCommitCount']
            )
            list.append(model)

        operations = []
        for model in list:
            operations.append(
                UpdateOne(
                    {'_id': model._id},  # 필터 조건
                    {'$set': model.to_dict()},         # 업데이트 내용
                    upsert=True            # 문서가 없으면 생성
                )
            )

        if operations:
            self.collection.bulk_write(operations)

    def delete(self, _id):
        self.collection.delete_one(
            { '_id': _id }
        )

userCommitCountRepository = UserCommitCountRepository(client=client)

