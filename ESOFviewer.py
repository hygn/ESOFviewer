import pycurl
import time
import wget
from urllib.parse import urlencode
from io import BytesIO
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
end = 0
if end == 0:
    url = input("url: ")
    JSEEEIONID = input("JSESSIONID: ")
    KHANUSER = input("KHANUSER: ")
    safedrive = input("safemode(y/n): ")
    if safedrive == "y" or safedrive == "n":
        pass
    else:
        safedrive = input("safemode(y/n): ")
#url =  ""
#JSEEEIONID = ""
#KHANUSER = ""
while True:
    if end == 1:
        url = input("url: ")
        safedrive = input("safemode(y/n): ")
        if safedrive == "y" or safedrive == "n":
            pass
        else:
            safedrive = input("safemode(y/n): ")
    cookie = "KHANUSER=" + KHANUSER + "; JSESSIONID=" + JSEEEIONID 
    dat = curl(url, "", cookie, False)
    print("main page loaded")
    cnts = dat.split('if( headerCntntsTyCode === "')[1].split('"')[0]
    #next load
    get = url.strip("https://hoc26.ebssw.kr/mypage/userlrn/userLrnView.do?")
    params = get.split("&")
    post_data = {
     'stepSn': params[1].split("=")[1] ,
     'sessSn': '' , 
     'atnlcNo': params[0].split("=")[1] , 
     'lctreSn': params[2].split("=")[1],
     'cntntsTyCode' : cnts}
    postfields = urlencode(post_data)
    dat = curl("https://hoc26.ebssw.kr/mypage/userlrn/userLrnMvpView.do", postfields, cookie, True)
    print("sub page loaded")
    #extract video info
    video = dat.split('src":"')[1].split('"')[0]
    revtime = dat.split('var revivTime = Number( "')[1].split('"')[0]
    #getjs
    get_data = {
     '_': str(time.time()).split(".")[0]}
    getfields = urlencode(get_data)
    curl("https://hoc26.ebssw.kr/js/require.js?"+getfields, "", cookie, False)
    curl("https://hoc26.ebssw.kr/js/egovframework/com/ebs/cmmn/common.js?"+getfields, "", cookie, False)
    print("js loaded")
    #startsig
    post_data = {
     'lctreSn': params[2].split("=")[1],
     'cntntsUseTyCode' : cnts}
    postfields = urlencode(post_data)
    curl("https://hoc26.ebssw.kr/esof/cmmn/cntntsUseInsert.do", postfields, cookie, True)
    print("start packet sent")
    #getvideo
    wget.download(video.replace("\\", ""), 'out.mp4')
    print("video downloaded")
    #studycheck
    i = 0
    postfields = urlencode(post_data)
    rep = int(str(int(revtime)/120).split(".")[0])
    rem = int(revtime) % 120
    if safedrive == "y":
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
            curl("https://hoc26.ebssw.kr/mypage/userlrn/lctreLrnSave.do", postfields, cookie, True)
            print("check packet sent")
            i = i + 1
            if i != rep:
                time.sleep(120)
            if i == rep:
                time.sleep(rem)
                post_data = {
                'stepSn': params[1].split("=")[1] ,
                'sessSn': '' , 
                'atnlcNo': params[0].split("=")[1] , 
                'lctreSn': params[2].split("=")[1],
                'cntntsTyCode' : cnts,
                'lctreSeCode' : 'LCTRE',
                'revivTime' : revtime ,
                'lastRevivLc' : revtime ,
                'lrnTime' : str(rem),
                'endButtonYn' :  'Y'
                 }
                postfields = urlencode(post_data)
                curl("https://hoc26.ebssw.kr/mypage/userlrn/lctreLrnSave.do", postfields, cookie, True)
                print("end packet sent")
                break
    else:
        goto = input("goto(seconds)(empty is goto end): ")
        if goto == "":
            goto = revtime
        else:
            pass
        post_data = {
        'stepSn': params[1].split("=")[1] ,
        'sessSn': '' , 
        'atnlcNo': params[0].split("=")[1] , 
        'lctreSn': params[2].split("=")[1],
        'cntntsTyCode' : cnts,
        'lctreSeCode' : 'LCTRE',
        'revivTime' : revtime ,
        'lastRevivLc' : str(120) ,
        'lrnTime' : str(120)}
        postfields = urlencode(post_data)
        curl("https://hoc26.ebssw.kr/mypage/userlrn/lctreLrnSave.do", postfields, cookie, True)
        print("check packet sent")
        time.sleep(10)
        post_data = {
        'stepSn': params[1].split("=")[1] ,
        'sessSn': '' , 
        'atnlcNo': params[0].split("=")[1] , 
        'lctreSn': params[2].split("=")[1],
        'cntntsTyCode' : cnts,
        'lctreSeCode' : 'LCTRE',
        'revivTime' : revtime ,
        'lastRevivLc' : goto,
        'lrnTime' : str(int(goto)%120),
        'endButtonYn' :  'Y'
         }
        postfields = urlencode(post_data)
        curl("https://hoc26.ebssw.kr/mypage/userlrn/lctreLrnSave.do", postfields, cookie, True)
        print("end packet sent")
    end = 1
