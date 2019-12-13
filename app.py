from flask import Flask, render_template, request
from decouple import config
import requests, pprint, random
app = Flask(__name__)


url = 'https://api.telegram.org'
token = config('TELEGRAM_BOT_TOKEN')
chat_id = config('CHAT_ID')


@app.route('/write')
def write():
    return render_template('write.html')


@app.route('/send')
def send():
    # 1. 사용자가 입력할 데이터 받아오기 
    text = request.args.get("message")

    # 2. 텔레그램 API 메세지 전송 요청 보내기
    send_message = requests.get(f'{url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')

    print(send_message.text)

    return '메세지 전송 완료!! :)'






#------------------------------문자보낸 사람에게 답장하기---------------------------------------#

@app.route('/answer')
def answer():
    return render_template('answer.html')


@app.route('/sendtoother')
def sendtoother():
    # 1. 사용자가 입력할 데이터 받아오기 
    text = request.args.get("message")

    chat_other_id = requests.get(f'{url}/bot{token}/getUpdates').json()["result"][-1]["message"]["from"]["id"]
    print(chat_other_id)

    # 2. 텔레그램 API 메세지 전송 요청 보내기
    requests.get(f'{url}/bot{token}/sendMessage?chat_id={chat_other_id}&text={text}')

    return '메세지 전송 완료!! :)'





#-------------------------------web hook 적용 ------------------------------#
'''단순 요청 응답 구조에서는 매크로를 이용해 계속 getUpdates를 해야하는 문제가 있다. 이를 보완해 web hook을 사용할 수 있다'''

'''
요청의 종류로, get 요청과 post 요청이 있다.
get : html 페이지 등의 정보를 주세요
Post: 당신측의 정보를 생성/수정 해주세요

여기서 POST를 사용하는 이유는, telegram 측이 web hook을 할 때 POST형태로 보내주도록 setting이 되어 있기 때문임


token은 web hook을 구현하기 위한 요소 중 하나이다. 타인에게는 공개하지 않는 token정보를 텔레그램 측에 알려주어, telegram만 알림을 전달하게 만들 수 있다.



텔레그램에게 전송하는 것
    return내용 : 텔레그램이 알림을 보내주면, 응답하는 구조인데 응답의 내용은 없으므로 '' 처리하고, 단, 전달을 잘 받은 경우 코드 200을 보내준다는 의미

'''

# @app.route(f'/{token}', methods=['POST'])
#  def telegram():
#      return '', 200


''' 메아리 기능 만들기'''
@app.route(f'/{token}', methods=['POST'])
def telegram():
    # 1. 텔레그램이 보내주는 데이터 구조 확인
    pprint.pprint(request.get_json())
    # 2. 사용자 아이디, 메세지 추출
    chat_id = request.get_json()["message"]["from"]["id"]
    message = request.get_json()["message"]["text"]
    # 3. 메아리 답장 보내기
    requests.get(f'{url}/bot{token}/sendMessage?chat_id={chat_id}&text={message}')
    return '', 200

'''로또라는 메시지를 받으면 로또 번호 6개 돌려주기'''

# @app.route(f'/{token}', methods=['POST'])
# def telegram():
#     # 1. 텔레그램이 보내주는 데이터 구조 확인
#     pprint.pprint(request.get_json())

#     # 2. 사용자 아이디, 메세지 추출
#     chat_id = request.get_json()["message"]["from"]["id"]
#     message = request.get_json()["message"]["text"]

#     # 로또 라고 입력하면 로또번호
#     if message == '로또':
#         result = random.sample(range(1,46),6)

#     # 그 외의 경우엔 메아리
#     else :
#         result = message

#     requests.get(f'{url}/bot{token}/sendMessage?chat_id={chat_id}&text={result}')
#     return '', 200




# --------------------------------------

@app.route('/')
def hello_world():
    return 'Hello World!'




### flask run 반복을 없애기 위한 코드

if __name__ == '__main__':
    app.run(debug=True)