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

    def __init__(self, _id, indices=[], updatedAt=datetime.now(timezone.utc), createdAt=datetime.now(timezone.utc)):
        self._id = _id
        self.openList = indices
        self.updatedAt = updatedAt
        self.createdAt = createdAt

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
