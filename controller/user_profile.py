from flask import Blueprint, render_template ,request, jsonify

bp = Blueprint('profile', __name__)

user_data = {       # 사용자 데이터를 저장할 변수 (임시 데이터베이스)
    'bio': '아보카도 맛있다.'
}

@bp.route('/profile')   # 프로필
def profile(): 
    return render_template('profile.html', bio=user_data['bio'])


@bp.route('/profile/modifi')    # 프로필 수정
def modifi_profile():
    return render_template('modifi_profile.html', bio=user_data['bio'])

@bp.route('/profile/save', methods=['POST'])   # 프로필 저장
def save_profile():
    data = request.get_json()
    user_data['bio'] = data.get('bio', user_data['bio'])
    return jsonify(success=True)