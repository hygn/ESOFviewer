# 왜 이런 문서를 만들었나요
* 억울하게 부적정수강 당해서
* 씨1발 듣지도 않았는데 왜 부적정수강인데
# 어케 알아냄?
* 개발자모드의 network탭
* mitmproxy를 사용한 패킷 분석
* 각 페이지의 소스 코드 분석
# 분석 내용
## URL
* *.ebssw.kr 에서 * = 서버 번호
## https://*.ebssw.kr/mypage/userlrn/userLrnView.do?atnlcNo=nnnnnn&stepSn=nnnnnn&lctreSn=nnnnnn&onlineClassYn=Y&returnUrl=
* 강의 메인 페이지
* 쿠키 (JSESSIONID, khanuser)
* GET요청
* if( headerCntntsTyCode === "~~~") 에서 cntntsTyCode를 구할 수 있음
## https://*.ebssw.kr/mypage/userlrn/userLrnMvpView.do
* 강의 정보
* 쿠키 (JSESSIONID, khanuser)
* POST 요청 (atnlcNo, stepSn, lctreSn, cntntsTyCode)
* atnlcNo, stepSn, lctreSn은 userLrnView.do로 전송된 GET 파라미터를 그대로 따라간다
* src:"~~~" 에서 동영상 URL을 구할 수 있음
* 유튜브인경우 &lt;iframe id="iframeYoutube" src="~~~"&gt; 에서 embed링크를 구할 수 있음
* 동영상 길이는 var revivTime = Number( "~~~" )에서 구할 수 있음
* &lt;strong class="content_tit"&gt;~~~&lt;/strong&gt; 사이에서 강의명을 구할 수 있음
## https://*.ebssw.kr/js/require.js?_=nnnnnn
* js
* GET요청
* nnnnnn은 요청시간의 unixtime(GMT)
## https://*.ebssw.kr/js/egovframework/com/ebs/cmmn/common.js?_=nnnnnn
* js
* GET요청
* nnnnnn은 요청시간의 unixtime(GMT)
## https://*.ebssw.kr/esof/cmmn/cntntsUseInsert.do
* 강의 접속 보고
* 쿠키 (JSESSIONID, khanuser)
* POST요청 (lctreSn, cntntsUseTyCode)
* lctreSn은 userLrnView.do로 전송된 GET파라미터를 그대로 따라간다
* cntntsUseTyCode 는 userLrnMvpView.do로 전송된 POST파라미터를 그대로 따라간다
## https://*.ebssw.kr/mypage/userlrn/lctreLrnSave.do
* 강의 진도율, 수강완료 보고
* 모든 시간은 초 단위를 사용함
* 쿠키 (JSESSIONID, khanuser)
### 강의 진도율 보고
* 강의 진도율 보고는 2분(120초)마다 이루어짐
* 요청 반복 횟수 = {(동영상 재생시간)-(동영상 재생시간)%120}/120 
  * %는 나머지를 뜻함
* POST요청 (stepSn, lrnAt, atnlcNo, lctreSn, cntntsTyCode, lctreSeCode, revivTime, lastRevivLc, lrnTime)
* atnlcNo, stepSn, lctreSn은 userLrnView.do로 전송된 GET 파라미터를 그대로 따라간다
* cntntsUseTyCode 는 userLrnMvpView.do로 전송된 POST파라미터를 그대로 따라간다
* lctreSeCode는 LCTRE로 고정된것으로 추정
* lrnAt는 처음 수강시 공백이며 두번쨰 수강부터 동영상 시작 시점이다 (동영상을 1500초부터 시청 => lrnAt: 1500)
* revivTime은 userLrnMvpView섹션에서 구한 동영상 길이이다
* lastRevivLc는 요청을 보내는 시점의 동영상 재생시간이다 (요청 전송시 동영상 2000초 시청 => lastRevivLc: 2000)
* lrnTime는 이전 강의 진도율 보고부터 현재 보고까지 걸린 시간이다. 강의 진도율 보고는 일반적으로 120초에 한번씩 이루어지므로, 일반적으로 120의 값을 갖는다
### 강의 완료 보고 
* POST요청 (stepSn, lrnAt, atnlcNo, lctreSn, cntntsTyCode, lctreSeCode, revivTime, lastRevivLc, lrnTime, endButtonYn)
* stepSn, lrnAt, atnlcNo, lctreSn, cntntsTyCode, lctreSeCode, revivTime 는 위와 같음
* lastRevivLc는 동영상 길이와 같음 
* lrnTime는 (동영상 길이)%120 이다
* endButtonYn은 수강완료 버튼을 눌렀을때 전송되며 일반적으로 Y 의 값을 갖는다
## 부적정수강 감지 방식(추정)
### 어케 알아냄?
* 직접 걸려보면서
* SNS게시글의 사례 분석
### 배속 , 매크로 감지
* 첫 진도율 보고와 강의 완료 보고 사이의 시간차를 구하는것으로 추정
* 첫 진도율 보고를 보내지 않고 강의 완료를 보고할경우 감지 되지 않는것으로 추정됨
* lrnTime이 불안정한 경우 감지 (일시정지할 경우 걸리는 이유로 추청됨)
### 동시수강 감지
* 동시에 다른 강의 창을 여는거까지는 가능
* 동시에 재생을 할 경우 강의 진도율 보고가 각각 다른 강의에서 동시에 가므로 감지 가능
