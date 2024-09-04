from flask import Blueprint, jsonify

from repository.dayTotalCommitCountRepository import dayTotalCommitCountRepository
from repository.userCommitCountRepository import userCommitCountRepository
from repository.repositoryProfile import profile_repository

bp = Blueprint('commit', __name__)

@bp.route('/commit/user/list')
def commitUserList():
    userCommitCountRepository # 오늘 유저들 가져옴 - 해당 idx로 user repo에서 가져옴 
    list = userCommitCountRepository.todayList()
    result = {
        "userList": [a.to_dict() for a in list]
    }
    return jsonify(result)

@bp.route('/commit/total-count')
def commitTotalCount():
    count = dayTotalCommitCountRepository.todayCount()
    result = {
        "commitTotalCount": count
    }
    return jsonify(result)

@bp.route('/commit/block-list')
def commitBlockList():
    return 'hello'

# @bp.route('/commit')
# def ():
#     return 'hello'