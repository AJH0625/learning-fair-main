from flask import Flask, request, redirect, jsonify, session, url_for, app
from flask_cors import CORS
from dotenv import load_dotenv
from markupsafe import escape
import os
import pymysql
from datetime import timedelta
import datetime
import lfmodules
import secrets

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False
app.secret_key = os.environ.get('FLASK_SESSION_SECRETKEY')

#테스트를 위한 값임.. 배포 시에는 minutes=10이 적당해보임
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=1)

like_button = 0

@app.route('/')
def index():
    if 'User_name' in session:
        global like_button
        like_button = 0
        return '로그인 성공! 아이디는 %s' % escape(session['User_name']) + \
            "<br><a href = '/logout'>로그아웃</a>"

    return lfmodules.template(lfmodules.getContents(), '<h2>Welcome to 2022 Learning Fair</h2>')


@app.route('/login', methods=['GET', 'POST'])
def login():
    sql = "INSERT INTO user (user_name, user_student_number, user_major, user_login_time, user_type) VALUES (%s, %s, %s, %s, %s)"
    if request.method == 'GET': 
        content = '''
            <form action="/login" method="POST">
                <p><input type="number" name="Student_ID" placeholder="Student_ID"></p>
                <p><input type="text" name="User_name" placeholder="User_name"></p>
                <p><input type="text" name="User_major" placeholder="User_major"></p>
                <p><input type="submit" value="로그인"></p>
            </form>
        '''
        return lfmodules.template(lfmodules.getContents(), content)
    elif request.method == 'POST':
        
        user_json = request.get_json()
        
        Student_ID = user_json['studentId']
        User_name = user_json['name']
        User_major = user_json['major']
        User_login_time = datetime.datetime.now()
        User_type = user_json['userType']

        User_token = secrets.token_hex(nbytes=32)

        #session[User_token] = user_json['name']
        session[user_json['name']] = user_json['userType']

        conn = pymysql.connect(host=os.environ.get('DB_URL'),
                       user=os.environ.get('DB_USER'),
                       password=os.environ.get('DB_PASSWORD'),
                       db=os.environ.get('DB_NAME'),
                       charset='utf8')

        with conn.cursor() as cur:
            cur.execute(sql, (User_name, Student_ID, User_major, User_login_time, User_type))
        conn.commit()
        
        return jsonify({"login":"success"})


@app.route('/session-check', methods=['POST'])
def session_check():
    print(session)

    session_check_json = request.get_json()

    if session_check_json['name'] in session:
        return jsonify({"session":"active"})
    else:
        return jsonify({"session":"deactive"})

@app.route('/congrats-videos')
def congrats_vidoes():
    #영상 업데이트 되면 url 바꿔야 함
    congrats_vidoes_json = {
        "president":"https://2022-skku-learning-fair-bucket.s3.ap-northeast-2.amazonaws.com/congrats/video1.mp4",
        "sw_dean":"https://2022-skku-learning-fair-bucket.s3.ap-northeast-2.amazonaws.com/congrats/video2.mp4",
        "ds_dean":"https://2022-skku-learning-fair-bucket.s3.ap-northeast-2.amazonaws.com/congrats/video3.mp4"
    }

    return jsonify(congrats_vidoes_json)

@app.route('/project-info', methods=['POST'])
def project_info():
    conn = pymysql.connect(host=os.environ.get('DB_URL'),
                       user=os.environ.get('DB_USER'),
                       password=os.environ.get('DB_PASSWORD'),
                       db=os.environ.get('DB_NAME'),
                       charset='utf8')

    project_info_request_json = request.get_json()
    sql = f"""SELECT * FROM project WHERE project_id = {project_info_request_json["project_id"]}"""

    with conn.cursor() as cur:
        cur.execute(sql)
    project_info_db_result = cur.fetchall()

    project_info_json = {
        "project_name":project_info_db_result[0][0],
        "team_name":project_info_db_result[0][1],
        "team_member":project_info_db_result[0][2],
        "class_name":project_info_db_result[0][3],
        "like_cnt":project_info_db_result[0][4],
        "hashtag_main":project_info_db_result[0][5],
        "hashtag_custom_a":project_info_db_result[0][6],
        "hashtag_custom_b":project_info_db_result[0][7],
        "hashtag_custom_c":project_info_db_result[0][8],
        "project_youtube_url":project_info_db_result[0][9],
        "project_pdf_url":project_info_db_result[0][10],
        "project_id":project_info_db_result[0][11],
        "team_number":project_info_db_result[0][12]
    }

    return jsonify(project_info_json)

@app.route('/tag')
def tag():
    tag = request.args.get('tag')
    if tag == None :
        content = '''
        <form action="/tag">
        <ol>
        <li><a href="?tag=1">운동</a></li>
        <li><a href="?tag=2">애니메이션</a></li>
        <li><a href="?tag=3">신입생</a></li>
        </ol>
        </form>
        '''
        return lfmodules.template(lfmodules.getContents(), content)
    else :
        content = f'''
        <h1>tag가 {tag}인 경우 데이터임.</h1>
        '''
        return lfmodules.templates(lfmodules.getTagContents(tag), content)


@app.route('/class/')
def class_():
    class_code = request.args.get('class')
    if class_code == None :
        content = '''
        <form action="/class/">
        <ol>
        <li><a href="?class='DASF_I1'">DASF_I1</a></li>
        <li><a href="?class='DASF_I2'">DASF_I2</a></li>
        <li><a href="?class='DASF_I3'">DASF_I3</a></li>
        </ol>
        </form>
        '''
        return lfmodules.template(lfmodules.getContents(), content)
    else :
        content = f'''
        <h1>class가 {class_code}인 경우 데이터임.</h1>
        '''
        return lfmodules.templates(lfmodules.getClassContents(class_code), content)


@app.route('/project/<int:id>/')
def project(id):
    Project =lfmodules.getProjects(id)
    title = Project[0][0]
    body = Project[0][10]
    return lfmodules.template(lfmodules.getContents(), f'<h2>{title}</h2>{body}')


@app.route('/project/<int:pj_id>/like/')
def like_project(pj_id):
    global like_button
    if like_button == 0:
        likeup= f"""
                UPDATE project
                set like_cnt = like_cnt + 1
                where project_id = {pj_id}
                """
        likecnts = f"""
                   SELECT like_cnt
                   FROM project
                   where project_id = {pj_id}
                   """
        with conn.cursor() as cur:
            cur.execute(likeup)
            cur.execute(likecnts)
            like_data = cur.fetchall()
        print(like_data[0][0])    
        like_button = 1
        return jsonify({'msg': '좋아요 완료!'})
    
    else :
        likeup= f"""
                UPDATE project
                set like_cnt = like_cnt - 1
                where project_id = {pj_id}
                """
        likecnts = f"""
                   SELECT like_cnt
                   FROM project
                   where project_id = {pj_id}
                   """
        with conn.cursor() as cur:
            cur.execute(likeup)
            cur.execute(likecnts)
            like_data = cur.fetchall()
        print(like_data[0][0])    
        like_button = 0
        return jsonify({'msg': '좋아요 취소!'})
    

@app.route('/logout')
def logout():
    session.pop('User_name', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)