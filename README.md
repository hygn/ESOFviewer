# Disclaimer
## USE AT YOUR OWN RISK
# EBS ESOF뷰어
코드 더럽습니다 보기전에 유의하세요
## Prerequirements
[Python, pip](https://www.python.org/downloads/)
## 사용방법
$ git clone https://gitlab.com/Hygn/esofviewer.git
(and cd into it)

$ pip3 install pycurl --user  
$ pip3 install wget --user  
$ pip3 install browser-cookie3 --user
$ python3 ESOFviewer.py   
강의 URL과 JSESSIONID,KHANUSER 쿠키를 입력하면 자동으로 시작합니다.  

Or if Windows Users, you can just run ESOFviewer_py.cmd
## 결과
강의 파일이 (강의 이름).mp4로 다운로드됩니다   
강의 시청 완료로 업데이트 됩니다   
safemode를 켜면 2분마다 저장 신호를 EBS에 보내며 강의 시간동안 계속 실행됩니다  
```
[esof@viewer esofviewer]$ python ESOFviewer.py
url: https://hoc.ebssw.kr/mypage/userlrn/userLrnView.do?atnlcNo=
brower(chrome, firefox): firefox
safemode(medium,strict): strict
main page loaded
sub page loaded
js loaded
start packet sent
download video? (y/n):n
skip video download
check packet sent
total time: 11 min 28 sec
time elapsed: 0 min
-----
check packet sent
total time: 11 min 28 sec
time elapsed: 2 min
-----
check packet sent
total time: 11 min 28 sec
time elapsed: 4 min
-----
check packet sent
total time: 11 min 28 sec
time elapsed: 6 min
-----
check packet sent
total time: 11 min 28 sec
time elapsed: 8 min
-----
check packet sent
total time: 11 min 28 sec
time elapsed: 10 min
-----
end packet sent
complete! 
 BanG Dream! 노래 정말 좋습니다. 꼭 들어보세요
```
## 기타
비정기적으로 업데이트합니다.  
EBS에서 POST요청부분과 서버 검증을 계속 바꿉니다.   
근데 몇글자만 추가하면 뚫림.  
나비보벳따우  
