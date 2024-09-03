from flask import Blueprint, render_template, request, jsonify
from repository.repositoryProfile import profile_repository

bp = Blueprint('profile', __name__)

# 외부에서 설정할 수 있는 testid
testid = None

def set_testid(tid):
    global testid
    testid = tid

@bp.route('/profile')  # 프로필
def profile():
    user_id = testid  # 실제 로그인된 유저의 ID로 대체해야 함
    user = profile_repository.read_all(user_id)
    
    if user:
        return render_template(
            'profile.html',
            pic_url=user.pic_url,
            generation=user.generation,
            num=user.num,
            name=user.name,
            bio=user.bio,
            like=user.like,
            git=user.git,
            commit=user.commit
        )
    else:
        return "User not found", 404

@bp.route('/profile/modifi')  # 프로필 수정
def modifi_profile():
    user_id = testid  # 실제 로그인된 유저의 ID로 대체해야 함
    user = profile_repository.read_all(user_id)

    if user:
         return render_template(
            'modifi_profile.html',
            pic_url=user.pic_url,
            generation=user.generation,
            num=user.num,
            name=user.name,
            bio=user.bio,
            like=user.like,
            git=user.git,
            commit=user.commit
        )
    else:
        return "User not found", 404

@bp.route('/profile/save', methods=['POST'])  # 프로필 저장
def save_profile():
    user_id = testid  # 실제 로그인된 유저의 ID로 대체해야 함
    data = request.get_json()
    bio = data.get('bio')

    if bio:
        profile_repository.update_bio(user_id, bio)
        return jsonify(success=True)
    else:
        return jsonify(success=False)

@bp.route('/profile/like', methods=['POST'])  # DB에 있는 like +1
def update_like():
    user_id = testid  # 실제 로그인된 유저의 ID로 대체해야 함
    
    # 데이터베이스에서 like 값을 증가시키고 업데이트된 like 값을 반환
    like = profile_repository.update_like_num(user_id)
    
    # profile_repository.delete_all()
    
    if like is not None:
        return jsonify(success=True, like=like)
    else:
        return jsonify(success=False), 404
