import pycurl
import time
import wget
from urllib.parse import urlencode
from io import BytesIO
import random
import browser_cookie3
import platform
buffer = BytesIO()


def curl(url, postfields, cookie, posten):
    curl = pycurl.Curl()
    curl.setopt(curl.URL, url)
    if posten:
        curl.setopt(curl.POSTFIELDS, postfields)
    else:
        pass
    curl.setopt(pycurl.COOKIE, cookie)
    curl.setopt(pycurl.USERAGENT,
                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0")
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
                    browser = input("brower(chrome, firefox): ")
                    if browser == "chrome" or browser == "firefox":
                        break
                    else:
                        pass
                else:
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
    ck1 = res[0].split(" ")[1].split(" ")[0]
    ck2 = res[1].split(" ")[1].split(" ")[0]
    cookie = ck1 + "; " + ck2
    dat = curl(url, "", cookie, False)
    print("main page loaded")
    cnts = dat.split('if( headerCntntsTyCode === "')[1].split('"')[0]
    # next load
    post_data = {
        'stepSn': params[1].split("=")[1],
        'sessSn': '',
        'atnlcNo': params[0].split("=")[1],
        'lctreSn': params[2].split("=")[1],
        'cntntsTyCode': cnts}
    postfields = urlencode(post_data)
    dat = curl("https://"+hoc+".ebssw.kr/mypage/userlrn/userLrnMvpView.do",
               postfields, cookie, True)
    print("sub page loaded")
    # extract video info
    video = dat.split('src":"')[1].split('"')[0]
    revtime = dat.split('var revivTime = Number( "')[1].split('"')[0]
    # getjs
    get_data = {
        '_': str(time.time()).split(".")[0]}
    getfields = urlencode(get_data)
    curl("https://"+hoc+".ebssw.kr/js/require.js?"+getfields, "", cookie, False)
    curl("https://"+hoc+".ebssw.kr/js/egovframework/com/ebs/cmmn/common.js?" +
         getfields, "", cookie, False)
    print("js loaded")
    # startsig
    post_data = {
        'lctreSn': params[2].split("=")[1],
        'cntntsUseTyCode': cnts}
    postfields = urlencode(post_data)
    curl("https://"+hoc+".ebssw.kr/esof/cmmn/cntntsUseInsert.do",
         postfields, cookie, True)
    print("start packet sent")
    # getvideo
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
                'lrnAt': '1',
                'atnlcNo': params[0].split("=")[1],
                'lctreSn': params[2].split("=")[1],
                'cntntsTyCode': cnts,
                'lctreSeCode': 'LCTRE',
                'revivTime': revtime,
                'lastRevivLc': str(120 * i),
                'lrnTime': str(120*lrnmux)}
            postfields = urlencode(post_data)
            curl("https://"+hoc+".ebssw.kr/mypage/userlrn/lctreLrnSave.do",
                 postfields, cookie, True)
            print("check packet sent")
            i = i + 1
            if i != rep:
                if safedrive == "strict":
                    time.sleep(120+random.randrange(0, 4)-2)
                elif safedrive == "off":
                    time.sleep(10)
                else:
                    rep = int((rep-rep%1.5)/1.5)
                    time.sleep(120+random.randrange(0, 4)-2)
            if i == rep:
                if safedrive == "strict":
                    time.sleep(rem)
                elif safedrive == "off":
                    time.sleep(10)
                else:
                    time.sleep(rem/1.5)
                post_data = {
                    'stepSn': params[1].split("=")[1],
                    'lrnAt': '1',
                    'atnlcNo': params[0].split("=")[1],
                    'lctreSn': params[2].split("=")[1],
                    'cntntsTyCode': cnts,
                    'lctreSeCode': 'LCTRE',
                    'revivTime': revtime,
                    'lastRevivLc': str(int(revtime)+random.randrange(0, 1)),
                    'lrnTime': str(rem),
                    'endButtonYn':  'Y'
                }
                postfields = urlencode(post_data)
                curl("https://"+hoc+".ebssw.kr/mypage/userlrn/lctreLrnSave.do",
                     postfields, cookie, True)
                print("end packet sent")
                break
    end = 1
    print("complete! \n BanG Dream! 노래 정말 좋습니다. 꼭 들어보세요")
except Exception as error:
    print("ERROR!!")
    print("please report this problem")
    print(error)
    input("")
    raise
