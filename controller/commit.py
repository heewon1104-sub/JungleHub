from flask import Blueprint, jsonify

from repository.dayTotalCommitCountRepository import dayTotalCommitCountRepository
from repository.userCommitCountRepository import userCommitCountRepository
from repository.repositoryProfile import profile_repository
from repository.boardBlockListRepository import boardBlockListRepository

bp = Blueprint('commit', __name__)

@bp.route('/commit/user/list')
def commitUserList():
    userCommitCountRepository  # 오늘 유저들 가져옴 - 해당 idx로 user repo에서 가져옴 
    try:
        todayCommitUserList = userCommitCountRepository.todayList()
    except Exception as e:
        print(f"Error fetching commit list: {e}")
        todayCommitUserList = []

    # 확인 로그 출력
    print(f"Today Commit User List: {todayCommitUserList}")
    
    userList = profile_repository.read_all_jungler()
    print(f"User List: {userList}")
    
    list = []
    for today in todayCommitUserList:
        for user in userList:
            if str(user._id) == str(today.userKey):
                list.append(
                    {
                        'user': user,
                        'count': today.count
                    }
                )

    if not list:
        print("No matching users found in the commit list.")

    list.sort(key=lambda item: (-item['count'], item['user'].id))
    result = {
        "userList": [ 
            { 
                "name": f'{item["user"].id}({item["user"].gitId}, {item["count"]})', 
                "id": item["user"]._id  
            } 
            for item in list
        ]
    }
    print(f"Final Result: {result}")
    return jsonify(result)


@bp.route('/commit/total-count')
def commitTotalCount():
    count = dayTotalCommitCountRepository.todayCumulative()
    result = {
        "commitTotalCount": count
    }
    return jsonify(result)


@bp.route('/commit/board/open/list')
def commitOpenList():
    item = boardBlockListRepository.todayOpenList()
    if item:
        result = {
            "indices": item.openList
        }
        return jsonify(result)
    else:
        return []

