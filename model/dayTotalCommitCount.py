from datetime import datetime, timezone, timedelta

class DayTotalCommitCount:

    @staticmethod
    def makeCurrentDayKey():
        current = datetime.now(timezone(timedelta(hours=9-6)))
        year = current.year
        month = current.month
        day = current.day
        return f"{year}-{month}-{day}"

    def __init__(self, _id, count=0, cumulativeCount = 0,updatedAt=None, createdAt=None):
        self._id = _id
        self.count = count
        self.cumulativeCount = cumulativeCount
        if updatedAt:
            self.updatedAt = updatedAt
        else:
            self.updatedAt = datetime.now(timezone.utc)
        if createdAt:
            self.createdAt = createdAt
        else:
            self.createdAt = datetime.now(timezone.utc)
    
    def to_dict(self):
        return {
            '_id': self._id,
            'count': self.count,
            'cumulativeCount': self.cumulativeCount,
            'updatedAt': self.updatedAt,
            'createdAt': self.createdAt,
        }

    @staticmethod
    def from_dict(data):
        _id = data.get('_id')
        count = data.get('count')
        cumulativeCount = data.get('cumulativeCount')
        updatedAt = data.get('updatedAt')
        createdAt = data.get('createdAt')

        return DayTotalCommitCount(_id=_id, count=count, cumulativeCount=cumulativeCount, updatedAt=updatedAt, createdAt=createdAt)
