from bson import ObjectId
from repository.repositoryConfig import client, RepositoryConfig
from datetime import datetime

class UserTable:
    def __init__(self, 
                 _id, 
                 id, 
                 nickname, 
                 pic_url, 
                 generation, 
                 num, 
                 name, 
                 like, 
                 gitId,
                 githubaccesstoken, 
                 git=None, 
                 bio=None):
        self._id = _id
        self.id = id
        self.nickname = nickname
        self.pic_url = pic_url
        self.generation = generation
        self.num = num
        self.name = name
        self.like = like
        self.git = git
        self.bio = bio
        self.gitId = gitId
        self.githubaccesstoken = githubaccesstoken

     # 객체를 딕셔너리로 변환하는 메서드
    def to_dict(self):
        return {
            "_id": self._id,
            "id": self.id,
            "pic_url": self.pic_url,
            "generation": self.generation,
            "num": self.num,
            "name": self.name,
            "like": self.like,
            "git": self.git,
            "bio": self.bio,
            "gitId": self.gitId,
            "githubaccesstoken": self.githubaccesstoken
        }
     
    def __repr__(self):
        return f"<UserTable(id={self.id}, name={self.name}, generation={self.generation})>"
    
class ProfileRepository:

    COLLECTION_NAME = 'user'

    def __init__(self, client):
        self.client = client
        self.db = client[RepositoryConfig.databaseName]
        self.collection = self.db[self.COLLECTION_NAME]

    # 새 유저 테이블 생성 함수
    def create(self, usertable):
        data = {
            "id": usertable.id,
            "nickname": usertable.nickname,
            "pic_url": usertable.pic_url,
            "generation": usertable.generation,
            "num": usertable.num,
            "name": usertable.name,
            "like": usertable.like,
            "git": usertable.git,
            "bio": usertable.bio,           # 자기소개
            "githubaccesstoken":usertable.githubaccesstoken,
            "gitId": usertable.gitId
        }
        result = self.collection.insert_one(data)
        usertable._id = str(result.inserted_id)  # MongoDB의 ObjectId를 문자열로 저장
        return usertable
    
    # 아이디를 기반으로 git, pic_url을 수정하는 함수
    def write_git_info(self, user_id, git_url, pic_url):
        result = self.collection.find_one_and_update(
            {'_id': ObjectId(user_id)},
            {'$set': {'git': git_url, 'pic_url': pic_url}},
            return_document=True
        )
        if result:
            return UserTable(
                _id=str(result['_id']),
                id=result['id'],
                nickname=result['nickname'],
                pic_url=result['pic_url'],
                generation=result['generation'],
                num=result['num'],
                name=result['name'],
                like=result['like'],
                git=result['git'],
                bio=result['bio'],
                githubaccesstoken=result['githubaccesstoken'],
                gitId=result['gitId']
            )
        return None
    

    # 데이터베이스의 모든 유저의 정보를 읽어오는 함수
    def read_all_jungler(self):
        junglerList = []
        cursor = self.collection.find()  # 모든 문서를 가져옴

        for data in cursor:
            usertable = UserTable(
                _id=str(data['_id']),
                id=data.get('id', ''),  # 'id' 필드가 없을 경우 빈 문자열을 사용
                nickname=data.get('nickname', ''),  # 'nickname' 필드가 없을 경우 빈 문자열을 사용
                pic_url=data.get('pic_url', ''),  # 'pic_url' 필드가 없을 경우 빈 문자열을 사용
                generation=data.get('generation', 0),  # 'generation' 필드가 없을 경우 기본값 0 사용
                num=data.get('num', 0),  # 'num' 필드가 없을 경우 기본값 0 사용
                name=data.get('name', ''),  # 'name' 필드가 없을 경우 빈 문자열 사용
                like=data.get('like', 0),  # 'like' 필드가 없을 경우 기본값 0 사용
                git=data.get('git', ''),  # 'git' 필드가 없을 경우 빈 문자열 사용
                bio=data.get('bio', ''),  # 'bio' 필드가 없을 경우 빈 문자열 사용
                githubaccesstoken=data.get('githubaccesstoken', ''),  # 'githubaccesstoken' 필드가 없을 경우 빈 문자열 사용
                gitId=data.get('gitId', '')  # 'gitId' 필드가 없을 경우 빈 문자열 사용
            )
            junglerList.append(usertable)
            #print(junglerList)

        return junglerList


    # _id를 기반으로 유저 테이블 정보를 읽어오는 함수
    def read_all(self, user_id):
        return self.collection.find_one({'_id': ObjectId(user_id)})
        # if data:
        #     usertable = UserTable(
        #         _id=data['_id'],
        #         id=data['id'],
        #         nickname=(data['nickname'], ''),
        #         pic_url=data['pic_url'],
        #         generation=data['generation'],
        #         num=data['num'],
        #         name=data['name'],
        #         like=data['like'],
        #         git=data['git'],
        #         bio=data['bio'],
        #         githubaccesstoken=data['githubaccesstoken'],
        #         gitId=data['gitId']
        #     )
        #     return usertable
        # return None
    
    # _id를 기반으로 bio 읽어서 return하는 함수
    def read_bio(self, user_id):
        data = self.collection.find_one({'_id': ObjectId(user_id)}, {'bio': 1})
        if data:
            return data['bio']
        return None
    
    def read_git_id(self, gitId):
        data = self.collection.find_one({ 'gitId': gitId })
        if data:
            return data['gitId']
        return None
    
    def read_git_user(self, git):
        data = self.collection.find_one({ 'git': git })
        if data:
            return data
        return None
    
    def read_github_access_token(self, accessToken):
        data = self.collection.find_one({ 'githubaccesstoken': accessToken })
        if data:
            return data
        return None
    

    # _id를 기반으로 like 읽어서 +1한 값으로 저장하고 like 값을 return
    def update_like_num(self, user_id):
        result = self.collection.find_one_and_update(
            {'_id': ObjectId(user_id)},
            {'$inc': {'like': 1}},  # like 필드를 1 증가시킴
            return_document=True  # 업데이트 후의 문서를 반환
        )
        if result:
            return result['like']  # 업데이트된 like 값을 반환
        return None

    # _id를 기반으로 bio를 수정하는 함수
    def update_bio(self, user_id, bio):
        result = self.collection.find_one_and_update(
            {'_id': ObjectId(user_id)},
            {'$set': {'bio': bio}},
            return_document=True
        )
        if result:
            return result['bio']
        return None
    
    def update_github_access_token(self, user, newAccessToken):
        result = self.collection.find_one_and_update(
            {'_id': user['_id'] },
            {'$set': { 'githubaccesstoken': newAccessToken }},
            return_document=True
        )
        if result:
            return result
        return None
    
    def delete(self, _id):
        if isinstance(_id) is not ObjectId:
            _id = ObjectId(_id)
        self.collection.delete_one(
            { '_id': _id }
        )

profile_repository = ProfileRepository(client)


class TokenTable:
    def __init__(self, 
                 userId, 
                 accesstoken, 
                 refreshtoken, 
                 updateat, 
                 createdat):
        self.userId = userId 
        self.accesstoken = accesstoken                  # jwt
        self.refreshtoken = refreshtoken                # jwt
        self.updateat = updateat
        self.createdat = createdat
     
    def __repr__(self):
        return f"<TokenTable(_id={self._id}, accesstoken={self.accesstoken})>"


class TokenRepository:
    def __init__(self, client):
        self.client = client
        self.db = client['dbjungle']
        self.collection = self.db['token']

    def delete(self, _id):
        if isinstance(_id) is not ObjectId:
            _id = ObjectId(_id)
        self.collection.delete_one(
            { '_id': _id }
        )

    # 새 유저 테이블 생성 함수
    def create(self, tokentable):
        data = {
            "userId": tokentable.userId,
            "accesstoken":tokentable.accesstoken,
            "refreshtoken":tokentable.refreshtoken,
            "updateat":tokentable.updateat,
            "createdat":tokentable.createdat
        }
        result = self.collection.insert_one(data)
        return tokentable
    
    # _id를 기반으로 updateat을 수정하는 함수
    def update_updateat(self, userId): 
        result = self.collection.find_one_and_update(
            {'userId': userId},
            {'$set': {'updateat': datetime.now()}},
            return_document=True
        )
        if result:
            return result['updateat']
        return None
    
    # _id를 기반으로 accesstoken을 수정하는 함수
    def update_accesstoken(self, userId, accesstoken): 
        result = self.collection.find_one_and_update(
            {'userId': userId},
            {'$set': {'accesstoken': accesstoken}},
            return_document=True
        )
        if result:
            return result['accesstoken']
        return None
    
    # 데이터베이스의 모든 유저의 정보를 읽어오는 함수
    def read_all_jungler(self):
        junglerList = []
        cursor = self.collection.find()  # 모든 문서를 가져옴

        for data in cursor:
            tokentable = TokenTable(
                userId=data['userId'],
                accesstoken=data['accesstoken'],
                refreshtoken=data['refreshtoken'],
                updateat=data['updateat'],
                createdat=data['createdat']
            )
            junglerList.append(tokentable)

        return junglerList


    # 데이터베이스의 모든 유저의 _id, accesstoken 알아오는 함수
    # 프로필 조회
    def read_all_accesstoken(self):
        accesstokenList = []
        cursor = self.collection.find()  # 모든 문서를 가져옴

        for data in cursor:
            tokentable = TokenTable(
                userId=data['userId'],
                accesstoken=data['accesstoken'],
                refreshtoken=data['refreshtoken'],
                updateat=data['updateat'],
                createdat=data['createdat']

            )
            accesstokenList.append(tokentable)
            
        return accesstokenList

    def read_all_token(self, user_id):
        data = self.collection.find_one({'userId': str(user_id)})
        if data:
            tokentable = TokenTable(
                userId=data['userId'],
                accesstoken=data['accesstoken'],
                refreshtoken=data['refreshtoken'],
                updateat=data['updateat'],
                createdat=data['createdat']
            )
            return tokentable
        return None
    

token_repository = TokenRepository(client)