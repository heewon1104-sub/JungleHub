from flask import Blueprint, render_template, request, jsonify, redirect, session
from module.githubApi import GithubApi
from module.InMemoryCache import inMemoryCacheInstance
import hashlib

bp = Blueprint('signup', __name__)


githubApi = GithubApi()

@bp.route("/signup", methods=['GET'])
def signup():
    # 사용자가 처음으로 접근하면 GitHub 로그인 페이지로 리다이렉트
    if 'access_token' not in session:
        githubLoginUrl = githubApi.getLoginUrl()
        return redirect(githubLoginUrl)
    else:
        # GitHub 인증 후 access_token이 세션에 저장되면 회원가입 페이지를 띄움
        return render_template('signup.html')

@bp.route("/signup/update", methods=['POST'])
def signupUpdate():
    id = request.form['id']
    password = request.form['password']
    passwordconfirm = request.form['password-confirm']
    cardinal = request.form['cardinal']
    number = request.form['number']
    intro = request.form['intro']

    # GitHub 인증이 완료되었음을 세션에서 확인할 수 있습니다.
    accessToken = session.get('access_token')

    # if not accessToken:
    #     return "GitHub 인증이 필요합니다.", 401

    # 여기에 추가로 사용자 데이터를 처리하는 코드를 작성합니다.
    # 예: 사용자 정보를 데이터베이스에 저장.

    return redirect('/main')

@bp.route("/signup/complete", methods=["GET"])
def signupComplete():
    
    code = request.args.get('code')
    
    if code:
        accessToken = githubApi.getAccessToken(code)
        print(accessToken)

        # GitHub로부터 받은 access token을 세션에 저장하거나, 필요한 처리를 합니다.
        session['access_token'] = accessToken

        # 이후 signup.html 페이지로 리다이렉트합니다.
        return redirect('/signup')
    else:
        return "GitHub 인증 실패", 400
    # TODO: 회원가입 처리!
    
    # 회원 create 
    # github access token도 함께 저장
    
    # JWT 만들기 - 뭐 들어갈지도 정해야 함. 
    # JWT를 clientInfo의 access_token에 할당

    clientInfo = {
        'access_token': 'access 토큰 입니다.'
    }

    # main 화면에서 사용할 client 정보.
    # clientInfo = { 'access_token': 'access 토큰 입니다.' }
    # print(str(clientInfo))
    # key = hashlib.sha256(str(clientInfo).encode()).hexdigest()
    # inMemoryCacheInstance.set(key, clientInfo)

    # TODO: batch refresh 해줘야 한다!!

    # # redirect할 때 hash key를 param으로 넣어준다. 
    # # 시간 + accessToken -> 이 값으로 캐시에서 값을 가져와서 해결

    # return redirect(f'/main?code={key}')
