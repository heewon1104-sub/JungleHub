from flask import Blueprint, render_template, redirect, request, jsonify
from module.InMemoryCache import inMemoryCacheInstance
from repository.dayTotalCommitCountRepository import dayTotalCommitCountRepository
from repository.userCommitCountRepository import userCommitCountRepository
from repository.repositoryProfile import profile_repository
from repository.boardBlockListRepository import boardBlockListRepository

bp = Blueprint('main', __name__)

@bp.route("/")
def root():
    return redirect('/main')

@bp.route("/main")
def main():
    code = request.args.get('code')
    clientInfo = inMemoryCacheInstance.get(code)
    inMemoryCacheInstance.delete(code)

    # 오늘 Commit한 유저들의 정보를 가져옴
    try:
        todayCommitUserList = userCommitCountRepository.todayList()
    except Exception as e:
        print(f"Error fetching commit list: {e}")
        todayCommitUserList = []

    # 모든 유저들의 정보를 읽어 userList에 저장
    userList = profile_repository.read_all_jungler()

    commit_list = []
    for today in todayCommitUserList:
        for user in userList:
            # 오늘 커밋을 한 유저면 commit_list에 user와 오늘 커밋 개수를 가져옴
            if str(user._id) == str(today.userKey):
                commit_list.append(
                    {
                        'user': user,
                        'count': today.count
                    }
                )

    # 커밋된 것이 없으면 아래 문자열 반환
    if not commit_list:
        print("No matching users found in the commit list.")

    # 커밋 수에 따라 내림차순 정렬
    commit_list.sort(key=lambda item: (-item['count'], item['user'].id))

    # 유저들의 누적 커밋수 가져옴
    count = dayTotalCommitCountRepository.todayCumulative()

    # boardBlockListRepository에서 오늘 오픈된 타일 인덱스 가져옴
    item = boardBlockListRepository.todayOpenList()
    open_list = item.openList if item else []

    # 템플릿으로 넘겨줄 데이터(유저 닉네임, 유저 아이디, 커밋수, 오늘 오픈된 타일 인덱스)
    result = {
        "userList": [ 
            { 
                "name": f'{item["user"].id}({item["user"].gitId}, {item["count"]})', 
                "id": item["user"]._id  
            } 
            for item in commit_list
        ],
       "commitTotalCount": count,
       "openListIndices": open_list
    }
    # clientInfo와 commit list를 템플릿으로 전달
    if clientInfo is not None:
        return render_template('main.html', clientInfo=clientInfo, users=result['userList'], openList=result['openListIndices'], totalCount=result['commitTotalCount'])
    else:
        return render_template('main.html', users=result['userList'], openList=result['openListIndices'],totalCount=result['commitTotalCount'])
