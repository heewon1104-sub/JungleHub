from datetime import datetime, timezone

class UserCommitCount():

    @staticmethod
    def makeCurrentDayUserKey(userId):
        current = datetime.now(timezone.utc)
        year = current.year
        month = current.month
        day = current.day
        return f"{year}-{month}-{day}-{userId}"

    def __init__(self, _id, userKey, count, updatedAt=datetime.now(timezone.utc), createdAt=datetime.now(timezone.utc)):
        self._id = _id 
        self.userKey = userKey
        self.count = count
        self.updatedAt = updatedAt
        self.createdAt = createdAt

    def to_dict(self):
        return {
            '_id': self._id,
            'userId': self.userId,
            'count': self.count,
            'updatedAt': self.updatedAt,
            'createdAt': self.createdAt,
        }

    @staticmethod
    def from_dict(data):
        _id = data.get('_id')
        userKey = data.get('userKey')
        count = data.get('count')
        updatedAt = data.get('updatedAt')
        createdAt = data.get('createdAt')

        return UserCommitCount(_id=_id, userKey=userKey, count=count, updatedAt=updatedAt, createdAt=createdAt)


