import pycurl
import time
import wget
from urllib.parse import urlencode
from io import BytesIO
import random
import subprocess
buffer = BytesIO()
def curl(url, postfields, cookie, posten):
    curl = pycurl.Curl()
    curl.setopt(curl.URL, url)
    if posten:
        curl.setopt(curl.POSTFIELDS, postfields)
    else:
        pass
    curl.setopt(curl.COOKIE, cookie)
    curl.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0")
    curl.setopt(pycurl.WRITEDATA, buffer)
    curl.setopt(pycurl.SSL_VERIFYPEER, 0)   
    curl.setopt(pycurl.SSL_VERIFYHOST, 0)
    curl.perform()
    curl.close()
    dat = buffer.getvalue().decode('UTF-8')
    return dat
def sendnoti(msg):
    subprocess.Popen(['notify-send', msg])
    return
end = 0
while True:
    if end == 0:
        try:
            url = input("url: ")
            print("input cookies (empty is use saved cookies)")
            JSEEEIONID = input("JSESSIONID: ")
            KHANUSER = input("KHANUSER: ")
            hoc = url.split("//")[1].split(".")[0]
            safedrive = input("safemode(y/n): ")
            if safedrive == "y" or safedrive == "n":
                pass
            else:
                 safedrive = input("safemode(y/n): ")
            break
        except IndexError:
            print("please input valid value!")
#url =  ""
#JSEEEIONID = ""
#KHANUSER = ""
if end == 1:
    while True:
        try:
            url = input("url: ")
            hoc = url.split("//")[1].split(".")[0]
            safedrive = input("safemode(y/n): ")
            if safedrive == "y" or safedrive == "n":
                pass
            else:
                safedrive = input("safemode(y/n): ")
            break
        except IndexError: 
            print("please input valid value!")
try:
    get = url.strip("https://"+hoc+".ebssw.kr/mypage/userlrn/userLrnView.do?")
    params = get.split("&")
    cookie = "KHANUSER=" + KHANUSER + "; JSESSIONID=" + JSEEEIONID 
    while True:
        try:
            f = open("cookies.cfg", "r+")
            if JSEEEIONID == "" or KHANUSER =="":
                cookie = f.read()
                break
            else:
                f.write(cookie)
                break
        except:
            f = open("cookies.cfg", "x")
            f.close()
    dat = curl(url, "", cookie, False)
    print("main page loaded")
    cnts = dat.split('if( headerCntntsTyCode === "')[1].split('"')[0]
    #next load
    post_data = {
     'stepSn': params[1].split("=")[1] ,
     'sessSn': '' , 
     'atnlcNo': params[0].split("=")[1] , 
     'lctreSn': params[2].split("=")[1],
     'cntntsTyCode' : cnts}
    postfields = urlencode(post_data)
    dat = curl("https://"+hoc+".ebssw.kr/mypage/userlrn/userLrnMvpView.do", postfields, cookie, True)
    print("sub page loaded")
    #extract video info    
    video = dat.split('src":"')[1].split('"')[0]
    revtime = dat.split('var revivTime = Number( "')[1].split('"')[0]
    #getjs
    get_data = {
     '_': str(time.time()).split(".")[0]}
    getfields = urlencode(get_data)
    curl("https://"+hoc+".ebssw.kr/js/require.js?"+getfields, "", cookie, False)
    curl("https://"+hoc+".ebssw.kr/js/egovframework/com/ebs/cmmn/common.js?"+getfields, "", cookie, False)
    print("js loaded")
    #startsig
    post_data = {
     'lctreSn': params[2].split("=")[1],
     'cntntsUseTyCode' : cnts}
    postfields = urlencode(post_data)
    curl("https://"+hoc+".ebssw.kr/esof/cmmn/cntntsUseInsert.do", postfields, cookie, True)
    print("start packet sent")
    #getvideo
    sendnoti("download video? \n please open command prompt")
    getvid = input("download video? (y/n):")
    if getvid == "y" or getvid == "n":
        pass
    else:
        getvid = input("download video?(y/n): ")
    if getvid == "y":
        wget.download(video.replace("\\", ""), 'out.mp4')
        print("video downloaded")
    else:
        print("skip video download")
    #studycheck
    i = 0
    postfields = urlencode(post_data)
    rep = int(str(int(revtime)/120).split(".")[0])
    rem = int(revtime) % 120
    if True:
        while True:
            if i == 0:
                lrnmux = 0
            else:
                lrnmux = 1
            post_data = {
            'stepSn': params[1].split("=")[1] ,
            'sessSn': '' , 
            'atnlcNo': params[0].split("=")[1] , 
            'lctreSn': params[2].split("=")[1],
            'cntntsTyCode' : cnts,
            'lctreSeCode' : 'LCTRE',
            'revivTime' : revtime ,
            'lastRevivLc' : str(120 * i) ,
            'lrnTime' : str(120*lrnmux)}
            postfields = urlencode(post_data)
            curl("https://"+hoc+".ebssw.kr/mypage/userlrn/lctreLrnSave.do", postfields, cookie, True)
            print("check packet sent")
            i = i + 1
            if i != rep:
                if safedrive == "y":
                    time.sleep(120+random.randrange(0,4)-2)
                if safedrive == "n":
                    time.sleep(10)
            if i == rep:
                if safedrive == "y":
                    time.sleep(rem)
                else:
                    time.sleep(10)
                post_data = {
                'stepSn': params[1].split("=")[1] ,
                'sessSn': '' , 
                'atnlcNo': params[0].split("=")[1] , 
                'lctreSn': params[2].split("=")[1],
                'cntntsTyCode' : cnts,
                'lctreSeCode' : 'LCTRE',
                'revivTime' : revtime ,
                'lastRevivLc' : str(int(revtime)+random.randrange(0,1)) ,
                'lrnTime' : str(rem),
                'endButtonYn' :  'Y'
                 }
                postfields = urlencode(post_data)
                curl("https://"+hoc+".ebssw.kr/mypage/userlrn/lctreLrnSave.do", postfields, cookie, True)
                print("end packet sent")
                sendnoti("complete! \n put another URL!")
                break
    end = 1
except Exception as error: 
    print("ERROR!!")
    print("please report this problem")
    print(error)
    input("")