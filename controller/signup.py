from flask import Blueprint, render_template, request, jsonify, redirect, session
from module.githubApi import GithubApi

bp = Blueprint('signup', __name__)

githubApi = GithubApi()

@bp.route("/signup", methods=['GET'])
def signup():
    return render_template('signup.html')

@bp.route("/signup/update", methods=['POST'])
def signupUpdate():
    id = request.form['id'],
    password = request.form['password']
    passwordconfirm = request.form['password-confirm']
    cardinal = request.form['cardinal']
    number = request.form['number']
    intro = request.form['intro']

    githubLoginUrl = githubApi.getLoginUrl()
    return redirect(githubLoginUrl)

@bp.route("/signup/complete", methods=["GET"])
def signupComplete():
    
    code = request.args.get('code')
    
    accessToken = githubApi.getAccessToken(code)

    print(accessToken)

    # TODO: 회원가입 처리!
    
    # 회원 create 
    # github access token도 함께 저장
    
    # JWT 만들기 - 뭐 들어갈지도 정해야 함. 
    # JWT를 clientInfo의 access_token에 할당

    clientInfo = {
        'access_token': 'access 토큰 입니다.'
    }

    session['clientInfo'] = clientInfo

    return redirect('/main')
