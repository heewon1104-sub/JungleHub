from datetime import datetime, timezone

class DayTotalCommitCount:

    @staticmethod
    def makeCurrentDayKey():
        current = datetime.now(timezone.utc)
        year = current.year
        month = current.month
        day = current.day
        return f"{year}-{month}-{day}"

    def __init__(self, _id, count=0, updatedAt=datetime.now(timezone.utc), createdAt=datetime.now(timezone.utc)):
        self._id = _id
        self.count = count
        self.updatedAt = updatedAt
        self.createdAt = createdAt
    
    def to_dict(self):
        return {
            '_id': self._id,
            'count': self.count,
            'updatedAt': self.updatedAt,
            'createdAt': self.createdAt,
        }

    @staticmethod
    def from_dict(data):
        _id = data.get('_id')
        count = data.get('count')
        updatedAt = data.get('updatedAt')
        createdAt = data.get('createdAt')

        return DayTotalCommitCount(_id=_id, count=count, updatedAt=updatedAt, createdAt=createdAt)
