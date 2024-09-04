from flask import Blueprint, render_template, request, jsonify, redirect, session
from module.githubApi import GithubApi
from module.InMemoryCache import inMemoryCacheInstance
import hashlib

bp = Blueprint('signup', __name__)

githubApi = GithubApi()

@bp.route("/signup", methods=['GET'])
def signup():
    return render_template('signup.html')

@bp.route("/signup/update", methods=['POST'])
def signupUpdate():
    id = request.form['id'],
    password = request.form['password']
    intro = request.form['intro']
    githubLoginUrl = githubApi.getLoginUrl()
    return redirect(githubLoginUrl)

@bp.route("/signup/complete", methods=["GET"])
def signupComplete():
    
    code = request.args.get('code')
    
    accessToken = githubApi.getAccessToken(code)

    # TODO: 회원가입 처리!
    
    # 회원 create 
    # github access token도 함께 저장
    
    # JWT 만들기 - 뭐 들어갈지도 정해야 함. 
    # JWT를 clientInfo의 access_token에 할당


    # main 화면에서 사용할 client 정보.
    clientInfo = { 'access_token': 'access 토큰 입니다.' }
    print("💩")
    print(str(clientInfo))
    key = hashlib.sha256(str(clientInfo).encode()).hexdigest()
    inMemoryCacheInstance.set(key, clientInfo)


    # TODO: batch refresh 해줘야 한다!!

    # redirect할 때 hash key를 param으로 넣어준다. 
    # 시간 + accessToken -> 이 값으로 캐시에서 값을 가져와서 해결

    return redirect(f'/main?code={key}')
