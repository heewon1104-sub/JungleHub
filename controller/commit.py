from flask import Blueprint, jsonify

from repository.dayTotalCommitCountRepository import dayTotalCommitCountRepository
from repository.userCommitCountRepository import userCommitCountRepository
from repository.repositoryProfile import profile_repository

bp = Blueprint('commit', __name__)

@bp.route('/commit/user/list')
def commitUserList():
    userCommitCountRepository # 오늘 유저들 가져옴 - 해당 idx로 user repo에서 가져옴 
    todayCommitUserList = userCommitCountRepository.todayList()
    userList = profile_repository.read_all_jungler()
    list = []
    for today in todayCommitUserList:
        for user in userList:
            if user._id == today.userKey:
                list.append(user)
    result = {
        "userList": [ { "name": a.id + f'({a.gitId})', "id": a._id  } for a in list]
    }
    return jsonify(result)

@bp.route('/commit/total-count')
def commitTotalCount():
    count = dayTotalCommitCountRepository.todayCount()
    result = {
        "commitTotalCount": count
    }
    return jsonify(result)


@bp.route('/commit/board/open/list')
def commitOpenList():

    return