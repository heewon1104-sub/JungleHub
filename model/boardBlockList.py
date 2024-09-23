from datetime import datetime, timezone, timedelta
import json

class BoardBlockList:

    @classmethod
    def makeKey(self):
        current = datetime.now(timezone(timedelta(hours=9-6)))
        year = current.year
        month = current.month
        day = current.day
        return f"{year}-{month}-{day}"

    def __init__(self, _id, indices=[], updatedAt=None, createdAt=None):
        self._id = _id
        self.openList = indices
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
            'openList': json.dumps(self.openList),
            'updatedAt': self.updatedAt,
            'createdAt': self.createdAt,
        }

    @staticmethod
    def from_dict(data):
        _id = data.get('_id')
        openList = json.loads(data.get('openList'))
        updatedAt = data.get('updatedAt')
        createdAt = data.get('createdAt')

        return BoardBlockList(_id=_id, indices=openList, updatedAt=updatedAt, createdAt=createdAt)
