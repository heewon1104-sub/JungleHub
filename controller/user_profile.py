from flask import Blueprint, render_template, request, jsonify
from repository.repositoryProfile import profile_repository
from repository.repositoryProfile import token_repository
from module.InMemoryCache import inMemoryCacheInstance
import jwt


bp = Blueprint('profile', __name__)

SECRET_KEY = "MY_SECRET_KEY"  # JWT 토큰을 검증할 시크릿 키

@bp.route('/profile/info', methods=['GET'])  # 프로필
def profile():
  # 요청 헤더에서 Authorization 헤더로 accessToken 가져오기
    access_token = request.headers.get('Authorization')
    print(access_token)

    if not access_token:
        return "Access token is missing or invalid", 400
    

    # "Bearer " 부분 제거하고 토큰만 추출
    token = access_token.split("Bearer ")[-1]
    print(token)



    accesstokenList = token_repository.read_all_accesstoken()

     # 토큰 유효성 검증
    try:

        # 데이터베이스에서 해당 유저의 accesstoken을 조회하여 비교
        for token_entry in accesstokenList:
            if token_entry.accesstoken == token:
                userId = token_entry.userId
                junglerList = profile_repository.read_all_jungler()

                for profile in junglerList:
                    if profile._id == userId:
                        return jsonify(profile.to_dict()), 200

        # 토큰이 데이터베이스의 accesstoken과 일치하지 않으면 에러 반환
        return jsonify({"error": "Token is invalid"}), 401

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    


       






@bp.route('/profile', methods=['GET'])  # 프로필
def profile_test():
  return render_template('profile.html')
              
    
@bp.route('/profile/modifi')  # 프로필 수정
def modifi_profile():
    # 요청에서 'code' 파라미터 가져오기
    code = request.args.get('code')
    
    # 캐시에서 'code'에 해당하는 accessToken 가져오기
    myaccesstoken = inMemoryCacheInstance.get(code)

    if myaccesstoken is not None:
        # 모든 유저의 토큰 정보 읽어오기
        jungler_list = token_repository.read_all_jungler()

        # jungler_list에서 myaccesstoken과 일치하는 유저의 userId 찾기
        user_id = None
        for tokentable in jungler_list:
            if tokentable.accesstoken == myaccesstoken:
                user_id = tokentable.userId
                break  # 일치하는 유저를 찾으면 반복문 종료

        if user_id is None:
            return "User not found", 404

        # user_id를 기반으로 유저 정보 조회
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
    # 요청에서 'code' 파라미터 가져오기
    code = request.args.get('code')
    
    # 캐시에서 'code'에 해당하는 accessToken 가져오기
    myaccesstoken = inMemoryCacheInstance.get(code)

    if myaccesstoken is not None:
        # 모든 유저의 토큰 정보 읽어오기
        jungler_list = token_repository.read_all_jungler()

        # jungler_list에서 myaccesstoken과 일치하는 유저의 userId 찾기
        user_id = None
        for tokentable in jungler_list:
            if tokentable.accesstoken == myaccesstoken:
                user_id = tokentable.userId
                break  # 일치하는 유저를 찾으면 반복문 종료

        if user_id is None:
            return "User not found", 404

    data = request.get_json()
    bio = data.get('bio')

    if bio:
        profile_repository.update_bio(user_id, bio)
        return jsonify(success=True)
    else:
        return jsonify(success=False)

@bp.route('/profile/like', methods=['POST'])  # DB에 있는 like +1
def update_like():
   # 요청 헤더에서 Authorization 헤더로 accessToken 가져오기
    access_token = request.headers.get('Authorization')

    if not access_token:
        return jsonify(success=False, message="Access token is missing"), 400

    # 토큰 유효성 검증
    try:
        payload = jwt.decode(access_token, "MY_SECRET_KEY", algorithms=["HS256"])
        user_id = payload.get("userId")
        
        if not user_id:
            return jsonify(success=False, message="Invalid token"), 401

        # 데이터베이스에서 like 값을 증가시키고 업데이트된 like 값을 반환
        like = profile_repository.update_like_num(user_id)
        
        if like is not None:
            return jsonify(success=True, like=like)
        else:
            return jsonify(success=False), 404
    except jwt.ExpiredSignatureError:
        return jsonify(success=False, message="Token has expired"), 401
    except jwt.InvalidTokenError:
        return jsonify(success=False, message="Invalid token"), 401