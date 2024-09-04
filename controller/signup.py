from flask import Blueprint, render_template, request, redirect
from module.githubApi import GithubApi
from module.InMemoryCache import inMemoryCacheInstance
import hashlib
import jwt
from repository.repositoryProfile import profile_repository
from repository.repositoryProfile import token_repository
from repository.repositoryProfile import TokenTable
from repository.repositoryProfile import UserTable
from datetime import datetime

bp = Blueprint('signup', __name__)

githubApi = GithubApi()

@bp.route("/signup/redirect", methods=['GET'])
def singupRedirect():
    githubLoginUrl = githubApi.getLoginUrl()
    return redirect(githubLoginUrl)

@bp.route("/signup/complete", methods=["GET"])
def signupComplete():
    
    code = request.args.get('code')
    
    if code:
        accessToken = githubApi.getAccessToken(code)
        print(accessToken)

        # GitHub로부터 받은 access token을 세션에 저장하거나, 필요한 처리를 합니다.
        key = hashlib.sha256(accessToken.encode()).hexdigest()
        inMemoryCacheInstance.set(key, accessToken)
        # 이후 signup.html 페이지로 리다이렉트합니다.
        return redirect('/signup/?code={key}')
    else:
        return "GitHub 인증 실패", 400


@bp.route("/signup", methods=['GET'])
def signup():
    # 사용자가 처음으로 접근하면 GitHub 로그인 페이지로 리다이렉트
    code = request.args.get('code')
    return render_template('signup.html',code=code)
       
        
@bp.route("/signup/update", methods=['POST'])
def signupUpdate():
    code = request.args.get('code')
    access_token = inMemoryCacheInstance.get(code)

    id = request.form['id']
    password = request.form['password']
    passwordconfirm = request.form['password-confirm']
    cardinal = request.form['cardinal']
    number = request.form['number']
    intro = request.form['intro']

    # GitHub 인증이 완료되었음을 세션에서 확인할 수 있습니다.

    # 입력받은 데이터를 usertable DB에 저장
    usertable = UserTable(
        _id=None,  # MongoDB에서 자동 생성되므로 None으로 설정
        id = id,
        password = password,
        pic_url=None, # TODO : 해주세요......
        generation=cardinal,
        num=number,
        name=None, # TODO : 해주세요......
        like=0,
        git=None, # TODO : 해주세요......
        commit=None, # TODO : 해주세요......
        bio=intro,
        githubaccesstoken = access_token
    )
    created_user = profile_repository.create(usertable) 
    user_id = created_user._id
    print(f"생성된 유저의 _id: {user_id}")
 
    # jwt 토큰 발급
    payload = {"userId": user_id}
    secret_key = "my_secret_key"
    accessToken = jwt.encode(payload, secret_key, algorithm="HS256")
    refreshToken = jwt.encode(payload, secret_key, algorithm="HS256")
 
    # tokentable에 token정보 추가
    tokentable = TokenTable(
        userId = user_id,
        accesstoken = accessToken,
        refreshtoken = refreshToken,
        updateat = None,
        createdat = datetime.now()
    )
    created_token = token_repository.create(tokentable) 
    print(f"생성된 유저의 userId: {created_token.userId}")    

    # TODO: batch refresh 해줘야 한다!!

    return redirect('/main')
