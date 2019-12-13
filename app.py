from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'









### flask run 반복을 없애기 위한 코드

if __name__ == '__main__':
    app.run(debug=True)