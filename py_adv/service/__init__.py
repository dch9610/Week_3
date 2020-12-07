from flask import Flask, render_template, request, redirect
from flask import session, jsonify

# 앱 생성, 기타 설정 구성
def create_app():
    app = Flask(__name__)

    # 세션처리
    initSession(app)

    # 환경변수 로드
    initenvironment(app)

    # DB연결처리, 엔트리 포인트(Server.py)를 기준으로 경로설정
    from service.model import initDataBasePooling
    initDataBasePooling(app)

    # 블루프린트 -> 기능별 / 카테고리별 라우트 처리를 분리
    initBlueprint(app)

    # 라이프사이클 처리 -> 요청,응답을 컨트롤
    initLifecycle(app)

    return app




def initSession(app):
    # 서버측에 클라이언트 정보를 저장하여 접속 및 요청을 쉽게 컨트롤    
    app.secret_key = '' # 랜덤한 해시값을 기록
    pass

def initenvironment(app):
    pass

# model 폴더안에 구축
# def initDataBasePooling(app):

def initBlueprint(app):
    @app.route('/')
    def home():
        return '홈페이지'
    pass 

# flask 상에서 진행되는 모든 요청과 응답은 라이플싸이클 함수를 거친다.
def initLifecycle(app):

    @app.before_first_request
    def before_first_request():
        print('서버가 가동하고 최초 요청시 1회 반응한다.')

    @app.before_request
    def before_request():
        # 여기서 세션처리를 수행하여, 페이지가 많아도 간단하게 컨트롤 할수 있다.
        print('모든 요청은 여기를 거쳐간다.')
        

    @app.after_request
    def after_request(res):
        # 모든 응답, 혹은 특정 응답에 조작을 가하거나, 가감을 하고 싶다면 여기서 처리
        print('모든 응답이 지나가는 곳')
        return res

    @app.teardown_request
    def teardown_request(ex):
        # 클라이언트가 잘 받아서 처리했다.
        print('브라우저가 응답을 받고 랜더링해서 화면이 보인다면 (실행)')
        return ''

    @app.teardown_appcontext
    def teardown_appcontext(ex):
        # 한개의 요청이 완벽하게 처리되었음을 전개
        print('http 요청 컨텍스트가 종료되었다.')
    pass