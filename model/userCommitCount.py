from datetime import datetime, timezone, timedelta

class UserCommitCount():

    @staticmethod
    def makeCurrentDayUserKey(userKey): # _id로 사용 
        current = datetime.now(timezone(timedelta(hours=9+6)))
        year = current.year
        month = current.month
        day = current.day
        return f"{year}-{month}-{day}-{userKey}"

    def __init__(self, _id, userKey, count, updatedAt=datetime.now(timezone.utc), createdAt=datetime.now(timezone.utc)):
        self._id = _id 
        self.userKey = userKey
        self.count = count
        self.updatedAt = updatedAt
        self.createdAt = createdAt

    def to_dict(self):
        return {
            '_id': self._id,
            'userKey': self.userKey,
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


