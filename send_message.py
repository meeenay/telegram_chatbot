import requests
from decouple import config

# request가 필요

'''----------------------자기자신에게 답장하기---------------------------'''
# 파이선 코드를 이용해 메세지 보내는 코드를 연습


url = 'https://api.telegram.org'
token = config('TELEGRAM_BOT_TOKEN') # 처음에는 실제 token 주소를 쓰다가, 환경변수로 이후에 변경함
chat_id = config('CHAT_ID')
text = input('메세지를 입력하세요: ')

send_message = requests.get(f'{url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')

print(send_message.text)




'''-------------------------다른사람에게 답장하기---------------------------- '''
## 다른 사람이 메시지를 보냈을 때 ID를 따야 답장을 할 수 있다
## get updates 메서드에서 ID를 따올 수 있었다. 


'''

import requests
from decouple import config

url = 'https://api.telegram.org'
token = config('TELEGRAM_BOT_TOKEN')

# 가져온 웹 내용을 python으로 가져와야 한다. text()로 뽑으면 텍스트구조이므로 대신 json()으로 출력하자
chat_id = requests.get(f'{url}/bot{token}/getUpdates').json()["result"][-1]["message"]["from"]["id"]

text = input('메세지를 입력하세요: ')
send_message = requests.get(f'{url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')
print(send_message.text)

'''



'''------------------ 자신의 token 숨기기 --------------------'''

# 이 프로젝트에 필요한 환경변수를 받을 것이다.
# pip install python-decouple 

# app.py와 같은 루트에서 파일 생성 .env
# .gitignore의 설정 때문에 .env 파일은 github에 올라가지 않는다.  따라서 보안이 가능하다
# .env 내에 환경변수 만들기 (토큰, 아이디)
# 이 띄어쓰기와 싱글 쿼트 조심 할 것

