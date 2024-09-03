from flask import Flask, render_template

app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    # debug를 True로 세팅하면, 해당 서버 세팅 후에 코드가 바뀌어도 문제없이 실행됨. 
    app.run(host='127.0.0.1', port=8000, debug = True)


