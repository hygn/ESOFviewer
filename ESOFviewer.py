from __future__ import unicode_literals
import pycurl
import time
import wget
from urllib.parse import urlencode
from io import BytesIO
import random
import browser_cookie3
import platform
import youtube_dl
buffer = BytesIO()


def curl(url, postfields, cookie, posten, os, browser):
    curl = pycurl.Curl()
    curl.setopt(curl.URL, url)
    if posten:
        curl.setopt(curl.POSTFIELDS, postfields)
    else:
        pass
    curl.setopt(pycurl.COOKIE, cookie)
    if os == "windows":
        if browser == "chrome":
            curl.setopt(pycurl.USERAGENT,
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36")
        if browser== "firefox":
            curl.setopt(pycurl.USERAGENT,
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0")
    if os == "linux":
        if browser == "chrome":
            curl.setopt(pycurl.USERAGENT,
                   "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36")
        if browser== "firefox":
            curl.setopt(pycurl.USERAGENT,
                    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0")
    curl.setopt(pycurl.WRITEDATA, buffer)
    curl.setopt(pycurl.SSL_VERIFYPEER, 0)
    curl.setopt(pycurl.SSL_VERIFYHOST, 0)
    curl.perform()
    curl.close()
    dat = buffer.getvalue().decode('UTF-8')
    return dat


end = 0
while True:
    if end == 0:
        try:
            url = input("url: ")
            hoc = url.split("//")[1].split(".")[0]
            while True:
                if platform.system() == 'Linux':
                    OS = "linux"
                    browser = input("brower(chrome, firefox): ")
                    if browser == "chrome" or browser == "firefox":
                        break
                    else:
                        pass
                else:
                    OS = "windows"
                    browser = "chrome"
                    break
            while True:
                safedrive = input("safemode(off,medium,strict): ")
                if safedrive == "off" or safedrive == "medium" or safedrive == "strict":
                    break
                else:
                    pass
            break
        except IndexError:
            print("please input valid value!")
#url =  ""
#JSEEEIONID = ""
#KHANUSER = ""
try:
    get = url.strip("https://"+hoc+".ebssw.kr/mypage/userlrn/userLrnView.do?")
    params = get.split("&")
    if browser == "firefox":
        cjr = str(browser_cookie3.firefox(
            domain_name="ebssw.kr")).split(">, <")
    else:
        cjr = str(browser_cookie3.chrome(domain_name="ebssw.kr")).split(">, <")
    res = [i for i in cjr if hoc+".ebssw.kr" in i]
    cki = 0
    cookie = ""
    while cki != len(res):
        ck = res[cki].split(" ")[1].split(" ")[0]
        cookie = cookie + ck
        if cki + 1 == len(res):
            pass
        else: 
            cookie = cookie + ", "
        cki = cki+1
    dat = curl(url, "", cookie, False , OS, browser)
    print("main page loaded")
    cnts = dat.split('if( headerCntntsTyCode === "')[1].split('"')[0]
    killsw = dat.split('<!--')[1].split("-->")[0]
    if killsw == "kill":
        print("killswitch detected!")
        input("")
        exit()
    # next load
    post_data = {
        'stepSn': params[1].split("=")[1],
        'sessSn': '',
        'atnlcNo': params[0].split("=")[1],
        'lctreSn': params[2].split("=")[1],
        'cntntsTyCode': cnts}
    postfields = urlencode(post_data)
    dat = curl("https://"+hoc+".ebssw.kr/mypage/userlrn/userLrnMvpView.do",
               postfields, cookie, True, OS, browser)
    print("sub page loaded")
    # extract video info
    try:
        video = dat.split('src":"')[1].split('"')[0]
        vidtype = "ebs"
    except Exception:
        video = dat.split('<iframe id="iframeYoutube" src="')[1].split('"')[0]
        vidtype = "yt"
        pass
    revtime = dat.split('var revivTime = Number( "')[1].split('"')[0]
    name = dat.split('<strong class="content_tit">')[1].split("<")[0]
    # getjs
    get_data = {
        '_': str(time.time()).split(".")[0]}
    getfields = urlencode(get_data)
    curl("https://"+hoc+".ebssw.kr/js/require.js?"+getfields, "", cookie, False, OS, browser)
    curl("https://"+hoc+".ebssw.kr/js/egovframework/com/ebs/cmmn/common.js?" +
         getfields, "", cookie, False, OS, browser)
    print("js loaded")
    # startsig
    post_data = {
        'lctreSn': params[2].split("=")[1],
        'cntntsUseTyCode': cnts}
    postfields = urlencode(post_data)
    curl("https://"+hoc+".ebssw.kr/esof/cmmn/cntntsUseInsert.do",
         postfields, cookie, True, OS, browser)
    print("start packet sent")
    # getvideo
    getvid = input("download video? (y/n):")
    if getvid == "y" or getvid == "n":
        pass
    else:
        getvid = input("download video?(y/n): ")
    if getvid == "y":
        if vidtype == 'ebs':
            wget.download(video.replace("\\", ""), name+'.mp4')
            print("video downloaded")
        if vidtype == 'yt':
            ydl_opts = {}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video])
    else:
        print("skip video download")
    # studycheck
    i = 0
    postfields = urlencode(post_data)
    rep = int(str(int(revtime)/120).split(".")[0])
    rem = int(revtime) % 120
    encheck = True
    if encheck == True:
        while True:
            if i == 0:
                lrnmux = 0
            else:
                lrnmux = 1
            post_data = {
                'stepSn': params[1].split("=")[1],
                'lrnAt': '0',
                'atnlcNo': params[0].split("=")[1],
                'lctreSn': params[2].split("=")[1],
                'cntntsTyCode': cnts,
                'lctreSeCode': 'LCTRE',
                'revivTime': revtime,
                'lastRevivLc': str(120 * i),
                'lrnTime': str(120*lrnmux)}
            postfields = urlencode(post_data)
            curl("https://"+hoc+".ebssw.kr/mypage/userlrn/lctreLrnSave.do",
                 postfields, cookie, True, OS, browser)
            print("check packet sent")
            if i != rep:
                if safedrive == "strict":
                    time.sleep(120+random.randrange(0, 4)-2)
                elif safedrive == "off":
                    time.sleep(10)
                else:
                    rep = int((rep-rep % 1.4)/1.4)
                    time.sleep(120+random.randrange(0, 4)-2)
            if i == rep:
                if safedrive == "strict":
                    time.sleep(rem)
                elif safedrive == "off":
                    time.sleep(10)
                else:
                    time.sleep(rem/1.4)
                post_data = {
                    'stepSn': params[1].split("=")[1],
                    'lrnAt': '0',
                    'atnlcNo': params[0].split("=")[1],
                    'lctreSn': params[2].split("=")[1],
                    'cntntsTyCode': cnts,
                    'lctreSeCode': 'LCTRE',
                    'revivTime': revtime,
                    'lastRevivLc': str(int(revtime)),
                    'lrnTime': str(rem),
                }
                postfields = urlencode(post_data)
                curl("https://"+hoc+".ebssw.kr/mypage/userlrn/lctreLrnSave.do",
                     postfields, cookie, True, OS, browser)
                post_data.update({'endButtonYn':  'Y'})
                postfields = urlencode(post_data)
                #curl("https://"+hoc+".ebssw.kr/mypage/userlrn/lctreLrnSave.do",
                     #postfields, cookie, True, OS, browser)
                print("end packet sent")
                break
            i = i + 1
    end = 1
    print("complete! \n BanG Dream! 노래 정말 좋습니다. 꼭 들어보세요")
except Exception as error:
    print("ERROR!!")
    print("please report this problem")
    print(error)
    input("")
    raise
