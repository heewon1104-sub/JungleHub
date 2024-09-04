from flask import Flask
from controller import main, login, user_profile, signup
import os

app = Flask(__name__)

# 런타임 에러 방지
# 환경 변수에서 SECRET_KEY를 가져오거나, 없으면 기본 값을 설정
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# 블루프린트 등록 
app.register_blueprint(main.bp)
app.register_blueprint(login.bp)
app.register_blueprint(user_profile.bp)
app.register_blueprint(signup.bp)

if __name__ == '__main__':
    # debug를 True로 세팅하면, 해당 서버 세팅 후에 코드가 바뀌어도 문제없이 실행됨. 
    app.run(host='127.0.0.1', port=8000, debug = True)