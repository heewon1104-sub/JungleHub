from flask import Flask
from controller import main, login, user_profile
from repository.repositoryProfile import profile_repository
from repository.repositoryProfile import UserTable

app = Flask(__name__)

# test용 유저 정보 생성
# def create_test_user():
#     test_user = UserTable(
#         _id=None,  # MongoDB에서 자동 생성되므로 None으로 설정
#         id="testuser123",
#         password="password123",
#         pic_url="https://example.com/profile-pic.jpg",
#         generation=7,
#         num=3,
#         name="테스트이름",
#         like=1,
#         git="https://github.com/testuser",
#         commit=10,
#         bio="테스트 유저입니다."
#     )
    
#     # 유저 생성 및 _id 반환
#     created_user = profile_repository.create(test_user)
#     print(f"생성된 유저의 _id: {created_user._id}")

#     return created_user._id


# testid = create_test_user()
# 블루프린트 등록 전에 testid를 전달
# 프론트랑 연결되면 수정하기
user_profile.set_testid(0)


# 블루프린트 등록 
app.register_blueprint(main.bp)
app.register_blueprint(login.bp)
app.register_blueprint(user_profile.bp)
# TODO: sign_up

# def print_repository_size():
#     junglers = profile_repository.read_all_jungler()
#     print(f"디비 크기 {len(junglers)} users.")

# def delete_all_users():
#     deleted_count = profile_repository.delete_all_users()
#     print(f"Deleted {deleted_count} users from the profile repository.")

if __name__ == '__main__':
    # delete_all_users()
    # print_repository_size()
    # debug를 True로 세팅하면, 해당 서버 세팅 후에 코드가 바뀌어도 문제없이 실행됨. 
    app.run(host='127.0.0.1', port=8000, debug = True)

