from flask import Flask
from controller import main, login, user_profile, signup, commit
from flask_cors import CORS
from configuration.config import Config
from batch.CommitCountScheduler import CommitCountScheduler

config = Config()

if config.isDev():
    CommitCountScheduler().job()
else:
    CommitCountScheduler().run()

app = Flask(__name__)

CORS(app)

# 블루프린트 등록 
app.register_blueprint(main.bp)
app.register_blueprint(login.bp)
app.register_blueprint(user_profile.bp)
app.register_blueprint(signup.bp)
app.register_blueprint(commit.bp)   

if __name__ == '__main__':
    host = config.getHost()
    port = config.getPort()
    debug = config.isDev()
    app.run(host=host, port=port, debug = debug)