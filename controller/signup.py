from flask import Blueprint, render_template, request, jsonify, redirect
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
    intro = request.form['intro']
    githubLoginUrl = githubApi.getLoginUrl()
    return redirect(githubLoginUrl)

@bp.route("/signup/complete", methods=["GET"])
def signupComplete():
    print("complete로 들어오긴 했다. 🍎")
    code = request.args.get('code')
    accessToken = githubApi.getAccessToken(code)
    print(code, accessToken)

    # TODO: 이걸로 로그인 처리!

    return redirect('/')

