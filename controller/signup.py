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

from configuration.config import Config

from batch.CommitCountScheduler import CommitCountScheduler


bp = Blueprint('signup', __name__)

githubApi = GithubApi()

@bp.route("/signup/redirect")  
def singupRedirect():
    githubLoginUrl = githubApi.getLoginUrl()
    return redirect(githubLoginUrl)

@bp.route("/signup/complete", methods=["GET"])
def signupComplete():
    
    code = request.args.get('code')
    
    if code:
        githubAccessToken = githubApi.getAccessToken(code)

        githubUserInfo = githubApi.getUserInfo(githubAccessToken=githubAccessToken)

        if githubUserInfo is not None:  
            git = githubUserInfo['html_url']

            user = profile_repository.read_git_user(git)

            if user:
                if user['git'] == git: # 이미 회원 가입된 사람
                    profile_repository.update_github_access_token(user, githubAccessToken)
                    userid = user['_id']
                    
                    token = token_repository.read_all_token(userid)
                    if token:
                        accessToken = token.accesstoken 
                        key = hashlib.sha256(accessToken.encode()).hexdigest()
                        inMemoryCacheInstance.set(key, {
                            "access_token": accessToken
                        })
                        return redirect(f'/main?code={key}')
                else: 
                    return redirect('/main')

        # GitHub로부터 받은 access token을 세션에 저장하거나, 필요한 처리를 합니다.
        key = hashlib.sha256(githubAccessToken.encode()).hexdigest()
        inMemoryCacheInstance.set(key, githubAccessToken)
        # 이후 signup.html 페이지로 리다이렉트합니다.
        return redirect(f'/signup?code={key}')
    else:
        return "GitHub 인증 실패", 400


@bp.route("/signup", methods=['GET'])
def signup():
    # 사용자가 처음으로 접근하면 GitHub 로그인 페이지로 리다이렉트
    code = request.args.get('code')
    print(code)
    return render_template('signup.html',code=code)
       
        
@bp.route("/signup/update", methods=['POST'])
def signupUpdate():
  
    code = request.args.get('code')
    github_access_token = inMemoryCacheInstance.get(code)
    print(code)

    id = request.form['id']
    password = request.form['password']
    passwordconfirm = request.form['password-confirm']
    cardinal = request.form['cardinal']
    number = request.form['number']
    intro = request.form['intro']

    githubUserInfo = githubApi.getUserInfo(githubAccessToken=github_access_token)

    pic_url = ""
    name = ""
    git = ""
    gitId = ""
    if githubUserInfo is not None:
        pic_url = githubUserInfo['avatar_url']
        name = githubUserInfo['name']
        git = githubUserInfo['html_url']
        gitId = githubUserInfo['login']

        if profile_repository.read_git(git) == git:
            # git 로 검색해서 있으면 중복 처리
            return redirect(f'/signup/fail?message=aleady')

    # 입력받은 데이터를 usertable DB에 저장
    usertable = UserTable(
        _id=None,  # MongoDB에서 자동 생성되므로 None으로 설정
        id = id,
        password = password,
        pic_url=pic_url,
        generation=cardinal,
        num=number,
        name=name, 
        like=0,
        git=git, 
        gitId=gitId,
        bio=intro,
        githubaccesstoken = github_access_token
    )
    created_user = profile_repository.create(usertable) 
    user_id = created_user._id
    print("생성된 유저의 _id: {user_id}")
 
    # jwt 토큰 발급
    payload = {"userId": user_id}

    config =Config()
    secret_key = config.find("MY_SECRET_KEY")
    algo = config.find("SECRET_KEY_ALGO")
    accessToken = jwt.encode(payload, secret_key, algorithm=algo)
    refreshToken = jwt.encode(payload, secret_key, algorithm=algo)

    # tokentable에 token정보 추가
    tokentable = TokenTable(
        userId = user_id,
        accesstoken = accessToken,
        refreshtoken = refreshToken,
        updateat = None,
        createdat = datetime.now()
    )
    created_token = token_repository.create(tokentable) 
    print("생성된 유저의 userId: {created_token.userId}")    

    # count batch refresh 
    # CommitCountScheduler().job()

     # main 화면에 전달 
    key = hashlib.sha256(accessToken.encode()).hexdigest()
    clientInfo = {
        'access_token': accessToken
    }
    inMemoryCacheInstance.set(key, clientInfo)

    return redirect(f'/main?code={key}')


@bp.route("/signup/fail")
def sigonupFail():
    message = request.args.get('message')
    return render_template('signupFail.html', message="이미 가입된 아이디입니다.")
