#-*- coding:utf-8 -*-

# 업그레이드 타이핑 게임 제작
# 사운드 적용 및 DB 연동

import random
import time
import sys
######### 사운드 출력 필요 모듈
import winsound    #'''파이썬에 내장된 패키지<--소리 재생'''
import sqlite3
import datetime    #'''게임 시간 기록에 필요한 패키지'''

encodings = "cp949"

######### DB생성 & Autocommit
# 본인 DB 파일 경로
conn = sqlite3.connect('./resource/records.db', isolation_level=None)

######### Cursor연결
cursor = conn.cursor()

######### 테이블 생성(Datatype : TEXT NUMERIC INTEGER REAL BLOB)
cursor.execute(
    "CREATE TABLE IF NOT EXISTS records(id INTEGER PRIMARY KEY AUTOINCREMENT,cor_cnt INTEGER, record text, regdate text)"
)

'''AUTOINCREMENT : 삽입할 때 insert해주지 않아도, 저절로 1씩 증가 또는 지정한 수로 증가\
    cor_cnt:정답 개수, record : 결과 '''
'''실행 했을 때 에러 발생하면 안됨. 데이터베이스 생성됐는지 확인'''


############################# 추가 코드 ############################
# GameStart 클래스 생성
class GameStart:
    def __init__(self, user):
        self.user = user
        
    # 유저 입장 알림
    def user_info(self):
        print("User : {}님이 입장하였습니다.".format(self.user))
        print()
#####################################################################3
def random_list():
    list = []
    while True:
        k = random.randint(0,9)
        if k not in list:
            list.append(k)
        if len(list) == 6:
            break
    return list

words = []                                   # 영어 단어 리스트 생성

n = 1                                        # 게임 시도 횟수
cor_cnt = 0                                  # 정답 개수

try:
    word_f=open('./resource/word1.txt', 'r') # 문제 txt 파일 로드
except IOError:
    print("파일이 없습니다!! 게임을 진행할 수 없습니다!!")
for c in word_f:
     words.append(c.strip())
word_f.close()

data = []
data_a = []
if words==[]:                                #파일이 없을때 프로그램 종료
    sys.exit()
#print(words)                                 # 단어 리스트 확인

for line in words:
    key_value = line.strip().split(":")
    data.append(key_value[0])
    data_a.append(key_value[1])

quiz = data_a
meaning = data

user_name=input("Ready? Input Your name>> ")             # Enter Game Start! 
user=GameStart(user_name)                     #### GameStart의 user객체 생성
user.user_info()                              #### user 입장 알림 메서드 호출

start = time.time()                          # Start Time
k = random_list()
while n <=5:


    answer = input(f"{meaning[k[n]]} : ")
    if quiz[k[n]] == answer:     # 입력 확인(공백제거)
        ########### 정답 소리 재생
        winsound.PlaySound(
            './sound/good.wav',
            winsound.SND_FILENAME   #'''winsound의 PlaySound라는 클래스로 지정'''
            #'''SND_FILENAME을 직접 넣었음'''
        )
        ############
        print(">>Pass!\n")
        cor_cnt += 1                         # 정답 개수 카운트

    else:
        ########### 오답 소리 재생
        winsound.PlaySound(
            './sound/bad.wav',
            winsound.SND_FILENAME
        )
        ##################

        print(">>Wrong!\n")

    n = n + 1                                   # 다음 문제 전환

end = time.time()                            # End Time
et = end - start                             # 총 게임 시간

et = format(et, ".3f")                       # 소수 셋째 자리 출력(시간)

print()
print('--------------')


if cor_cnt >= 3:                             # 3개 이상 합격
    print("결과 : 합격")
else:
    print("불합격")

######### 결과 기록 DB 삽입
    '''data삽입 전에 먼저 기록테이블 구조 열어보기'''
cursor.execute(
    "INSERT INTO records('cor_cnt', 'record', 'regdate') VALUES (?, ?, ?)",
    (
        cor_cnt, et, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    )
)
'''ID는 오토 인크리먼트이므로 입력안해줘도 자동으로 db에서 연속된 숫자형으로 넣어줌'''
'''strftime('%Y-%m-%d %H:%M:%S') : 포맷 변환'''

'''게임 실행해서 db기록되는지 확인'''
######### 접속 해제
conn.close()

# 수행 시간 출력
print("게임 시간 :", et, "초", "정답 개수 : {}".format(cor_cnt))
