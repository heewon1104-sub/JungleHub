from repository.repositoryConfig import client, RepositoryConfig
from model.userCommitCount import UserCommitCount
from datetime import datetime, timezone


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
    
    def updateCount(self, userCommitCount, newCount):
        self.collection.update_one(
            {'_id': userCommitCount._id},
            {'$set': { 'count': newCount, 'updatedAt': datetime.now(timezone.utc) }}
        )

    def updateAllUserCount(self, userIdAndNewCountList):
        operations = []
        for _id, newCount in userIdAndNewCountList:
            operations.append(
                {
                    'updateOne': {
                        'filter': {'_id': _id},
                        'update': {'$set': {'count': newCount, 'updatedAt': datetime.now(timezone.utc)}}
                    }
                }
            )
        if operations:
            self.collection.bulk_write(operations)

    def delete(self, _id):
        self.collection.delete_one(
            { '_id': _id }
        )

userCommitCountRepository = UserCommitCountRepository(client=client)
