# 웹데이터 수집 
[1.요구사항 분석](#1.요구사항분석) <br>
[2.데이터 수집](#데이터수집-획득Lv2) <br>
[3.데이터 적재](#데이터-적재) <br>
[4.데이터 획득](#데이터획득_Lv3_WebScrapping) <br>
[5.자동화 설정](#자동화설정)

- 데이터 수집을 수행해서, 혼자 사용하면 (비공개, 상업적으로 이용하지 않는다) 문제가 없다
- 수집한 내용을 (공공데이터등을 제외) 공개/상업적 목적으로 이용하면 법의 제제를 받을수도 있다.

1. 요구사항 분석
2. 데이터 수집
    - 난이도에 따라 구성 분리
        - Lv1
            - 데이터를 제공받는 케이스
                - 공공데이터, 공모전 데이터(활용 한계), 연구기관 / 교육기관 제공
                - 사내 데이터 (회사 내부 데이터)
        - Lv2
            - open API가 존재하는 케이스
            - 인증키를 통해서, 하루에 적정량의 데이터를 질의하여 활용할수 있는 경우 
            - 데이터는 통상 JSON / XML로 제공 => 반정형 데이터
            - 공개되어 있지는 않지만, 웹을 분석하고 http로 통신되는 부분을 체킹하여 수집할수도 있다(합법적인가?)
                -> 와이어샤크 (프로그램) <- 서비스 구축하는 곳에서 https + 암호화
            <br>

        --------------이하는 웹에서 구할경우------------------------------    

        - Lv3
            - 해당 웹페이지에서 바로 데이터를 수집할 수 있다면?
            - Web Scarpping (웹 스크래핑)
            - request, bs4(beatiful soup)
            - 비정형 데이터 (날것의 데이터, 구조가 없는 데이터)
            
        - Lv4
            - 해당 웹페이지가 사용자와 인터렉션을 통해서(반응해서) 데이터가 노출된다
            - 더보기, 스크롤, 로그인, 검색 등등 케이스. ajax를 사용한 사이트
            - selenium(셀레니움) + 웹드라이버 (브라우저 회사별로 제공하는)
            - 매크로 (좋지못한 목적으로 사용하는 자동화 프로그램)
            - 고급기술 => proxy를 중계하여 작업을 요청한 클라이언트를 숨기는 기술
        
        - 자동화
            * os 레벨에서 자동으로 데이터를 수집하게 하는 활동을 작성 / 운용
            * Lv3/Lv4 같은 경우는 단시간에 빠른 접속을 지속적으로 시도하면 
                * 디도스로 간주 할 수 있기 때문에, 적절한 시간 조절
                * 고급(접속한 유저의 ip를 우회하여(플락시 서버 활용) 처리)
            
                <br>
            
    
3. 데이터 준비 / 전처리 /적재
    - 전처리, 정제, 적재
    - 이상치, 결측치 처리
<br>

4. 데이터 분석
    - EDA (탐색적 분석)
    - 인과분석
    - ...
<br>

5. 모델 구축
    - 통계 모델(모형)
    - 머신러닝 모델
    - 딥러닝 모델
6. 시스템 구축 / 서비스 구성 / 레포트 => 산출물
<br>


# 데이터수집 획득Lv2
## 사용기술
    - open API 필요
        * dev.naver.com or dev.kakao.com
    - Client ID : ... <br>
    - Client PW : ...
    - API 문서 : https://openapi.naver.com/v1/search/news
    - 검색 URL (응답 데이터 json) : https://openapi.naver.com/v1/search/news.json

    - 예시

```
curl "https://openapi.naver.com/v1/search/news.xml?query=%EC%A3%BC%EC%8B%9D&display=10&start=1&sort=sim" \
-H "X-Naver-Client-Id: {애플리케이션 등록 시 발급받은 client id 값}" \
-H "X-Naver-Client-Secret: {애플리케이션 등록 시 발급받은 client secret 값}" -v
```
    - request 모듈 필요 -> 통신수행(http)
        * get방식을 주로 사용
        * 개인별 인증키는 헤더에 숨겨서 전송

## 구현
    1. 필요한 모듈 가져오기
    2. 환경변수, 통신에 필요한 키를 정의
    3. URL 정의 (JSON)
    4. 파라미터 정의 (검색어가 한글인 경우, uft-8 인코딩 처리)
    5. 최종 GET방식으로 요청하는 url
    6. 통신 객체 생성
    7. 클라이언트 키, 보안키 생성
    8. 통신
    9. 응답코드 확인 -> 
        - 200 : 정상을 의미
        - 401 : 권한오류
        - 404 : 해당 페이지가 없다
        - 500 : 서버 내부 에러
    10. 응답 데이터를 JSON 객체로 로드 -> 딕셔너리, 리스트 조합 구성
    11. 파싱

## 데이터 적재
- 파일
    - csv, xlsx

- 데이터베이스 (스키미가 외부에 존재)
    - RDBMS
        - 기업형 DB, ms-sql, oracle
        - 현재 작업 기준에서는 코랩에서 작동시, 고정 IP나 도메인을 가진 데이터 베이스를 활용하여 저장해야한다.
            - aws
    - No-SQL
        - 몽고디비 -> 로그 저장

- 절차
    - 데이터 구조 : [ {}, {}, {}, ...] 준비
    - pandas를 이용하여 DataFrame 구성
    - pymysql + sqlalchemy 이용하여 접속
    - 데이터를 데이터베이스에 적재
    - 연결 종료
    
    
# 데이터획득_Lv3_WebScrapping
## 조건

- 수집하고자하는 데이터가 웹사이트에 게시되어 있다.
- Open Api가 없다
- 사이트에 접속만 하면 그냥 볼수 있다
    - 더보기 x, 로그인 x, 스크롤해야 정보가 추가로 나타나는 증상,...
- 패키지
    - Beautiful Soup (bs4)
- 대상 사이트
    - 프레임소스보기 선택 view-source:https://finance.naver.com/marketindex/exchangeList.nhn
<hr>

## 간단한 사이트에서 수집
- 1.모듈 가져오기
    - from bs4 import BeautifulSoup, from urllib.request import urlopen
- 2. 타겟 사이트 접속
    - target_site = 'https://finance.naver.com/marketindex/exchangeList.nhn'
    - res         = urlopen(target_site)
- 3. 응답받은 데이터 => html 데이터 (반정형 데이터)
    - soup = BeautifulSoup(res, 'html5lib'

### 요구사항
- 통화명, 매매기준율, 사실때, 보내실때, 통화 코드 추출
- 이런 데이터를 추출하기 위해서 사이트의 html의 구조를 꼼꼼하게 체크, 
    - 개발자도구 > Elements 파트에서 시뮬레이션을 통해서 특정한 것이 정확한지 체킹
- 반복적으로 등장하는 데이터 (rows, 리스트형태(tr, li 태그로 나열된 형태))
    - row 데이터 단위로 수집을 수행해야, 문제 없이 수집이 가능!
    - [{},{},{}, ...] 구조로 손쉽게 구성
<hr>
   
    

## 바이너리 파일(압축된 파일)을 다운로드해서 수집하는 케이스 
- 응용
    - 웹상에서 이미지 수집도 가능
- 목적
    - http://yann.lecun.com/exdb/mnist/ 접속
    - 데이터 4개 다운로드
        - train-images-idx3-ubyte.gz
    - 압축해제
    - 디코딩 수행
    - 원하는 데이터를 추출, 저장
<br>

1. 타겟 사이트 -> MNIST
    - target_site = 'http://yann.lecun.com/exdb/mnist/'

2. Web Scriping -> soup 생성
    - res  = urlopen(target_site)
    - soup = BeautifulSoup(res, 'html5lib' )

3. 파일을 다운로드 할 수 있는 문자열 추출 (리스트)

4. 파일 다운로드 (-import os, os.path_
    4-1. 저장할 파일 위치 선정 -> './data/mnist'
    4-2. 파일 저장 - savedPath 
        - 진행률 표시 (import tqdm.notebook)
        - 해당 파일 직접 요청 (import urllib.request as req)
5. 압축 데이터 해제
    - gz 파일
        - gzip모듈을 활용 (import gzip) 
<hr>

## 자동화설정
1. .ipynb 파일을 .py 파일로 변경
2. 파워프롬프트 실행후 
    - python ./~/xxx.py 실행하여 정상작동 되는지 확인
3. 작업 스케줄러 설정
    - 새 작업 만들기에서 이름과 내용 설정
4. 트리거 만들기 ex) 작업 반복 간격 5분, 기간 설정

5. 동작
    - 프로그램 / 스크립트에 C:\Users\pnu\anaconda3\pythonw.exe 입력 (pythonw의 위치)
    - 인수추가 : 실행하고자 하는 .py파일
    - 시작위치 : .py 파일이 존재하는 위치
