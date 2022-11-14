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

#테스트를 위한 값임.. 배포 시에는 minutes=20이 적당해보임
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
        sql = "INSERT INTO user (user_name, user_student_number, user_major, user_login_time, user_type, user_token) VALUES (%s, %s, %s, %s, %s, %s)"

        user_json = request.get_json()
        
        Student_ID = user_json['studentId']
        User_name = user_json['name']
        User_major = user_json['major']
        User_login_time = datetime.datetime.now()
        User_type = user_json['userType']

        User_token = secrets.token_hex(nbytes=32)

        conn = pymysql.connect(host=os.environ.get('DB_URL'),
                       user=os.environ.get('DB_USER'),
                       password=os.environ.get('DB_PASSWORD'),
                       db=os.environ.get('DB_NAME'),
                       charset='utf8')

        with conn.cursor() as cur:
            cur.execute(sql, (User_name, Student_ID, User_major, User_login_time, User_type, User_token))
        conn.commit()
        
        sql2 = f"""SELECT user_id FROM user WHERE user_token = '{User_token}'"""

        with conn.cursor() as cur:
            cur.execute(sql2)
        user_id_db_result = cur.fetchall()

        print(user_id_db_result)

        session[User_token] = user_id_db_result[0][0]

        return jsonify({"login":"success","token":User_token,"user_id":user_id_db_result[0][0]})



@app.route('/session-check', methods=['POST'])
def session_check():
    print(session)

    session_check_json = request.get_json()

    if session_check_json['token'] in session:
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
        #"project_pdf_url":project_info_db_result[0][10],
        "project_pdf_url":"https://2022-skku-learning-fair-bucket.s3.ap-northeast-2.amazonaws.com/test/%ED%94%BC%EC%A7%80%EC%BB%AC+%EC%BB%B4%ED%93%A8%ED%8C%85+%EC%A4%91%EA%B0%84+%EB%B0%9C%ED%91%9C.pdf",
        "project_id":project_info_db_result[0][11],
        "team_number":project_info_db_result[0][12]
    }

    return jsonify(project_info_json)



@app.route('/project-layout-info', methods=['POST'])
def project_layout_info():
    conn = pymysql.connect(host=os.environ.get('DB_URL'),
                       user=os.environ.get('DB_USER'),
                       password=os.environ.get('DB_PASSWORD'),
                       db=os.environ.get('DB_NAME'),
                       charset='utf8')

    project_layout_info_request_json = request.get_json()
    sql = f"""SELECT team_name, class_name, team_number FROM project WHERE project_id = {project_layout_info_request_json["project_id"]}"""
    with conn.cursor() as cur:
        cur.execute(sql)
    project_layout_info_db_result = cur.fetchall()

    project_layout_info_json = {
        "team_name":project_layout_info_db_result[0][0],
        "class_name":project_layout_info_db_result[0][1],
        "team_number":project_layout_info_db_result[0][2]
    }
    return jsonify(project_layout_info_json)



@app.route('/class')
def class_list():
    conn = pymysql.connect(host=os.environ.get('DB_URL'),
                       user=os.environ.get('DB_USER'),
                       password=os.environ.get('DB_PASSWORD'),
                       db=os.environ.get('DB_NAME'),
                       charset='utf8')

    class_name = request.args.get('class')

    sql = f"""SELECT team_name, team_member, team_number, hashtag_main, hashtag_custom_a, hashtag_custom_b, hashtag_custom_c,project_name,like_cnt,project_thumbnail_url,project_id  FROM project WHERE class_name = '{class_name}'"""
    sql_ = f"""SELECT team_name, team_member, team_number, hashtag_main, hashtag_custom_a, hashtag_custom_b, hashtag_custom_c,project_name,like_cnt,project_thumbnail_url,project_id  FROM project WHERE class_name = '{class_name}' ORDER BY RAND()"""
    with conn.cursor() as cur:
        cur.execute(sql)
        class_project_list_db_result = cur.fetchall()
    
    with conn.cursor() as cur:
        cur.execute(sql_)
        class_project_list_db_result_rand = cur.fetchall()
        
    class_project_list_json = {"projects":[],"projectsRand":[]}
    
    for class_project in class_project_list_db_result:
        project_container = {
            "team_name":class_project[0], 
            "team_member":class_project[1], 
            "team_number":class_project[2], 
            "hashtag_main":class_project[3], 
            "hashtag_custom_a":class_project[4], 
            "hashtag_custom_b":class_project[5], 
            "hashtag_custom_c":class_project[6],
            "project_name":class_project[7],
            "like_cnt":class_project[8],
            "project_thumbnail_url":class_project[9],
            "project_id":class_project[10]
        }
        class_project_list_json["projects"].append(project_container)
        
    for class_project in class_project_list_db_result_rand:
        project_container_rand = {
            "team_name":class_project[0], 
            "team_member":class_project[1], 
            "team_number":class_project[2], 
            "hashtag_main":class_project[3], 
            "hashtag_custom_a":class_project[4], 
            "hashtag_custom_b":class_project[5], 
            "hashtag_custom_c":class_project[6],
            "project_name":class_project[7],
            "like_cnt":class_project[8],
            "project_thumbnail_url":class_project[9],
            "project_id":class_project[10]
        }
        
        class_project_list_json["projectsRand"].append(project_container_rand)

    return jsonify(class_project_list_json)

@app.route('/tag')
def tag_list():
    conn = pymysql.connect(host=os.environ.get('DB_URL'),
                       user=os.environ.get('DB_USER'),
                       password=os.environ.get('DB_PASSWORD'),
                       db=os.environ.get('DB_NAME'),
                       charset='utf8')

    tag_code = request.args.get('tag')

    sql = f"""SELECT team_name, team_member, team_number, hashtag_main, hashtag_custom_a, hashtag_custom_b, hashtag_custom_c FROM project WHERE hashtag_main = '{tag_code}' ORDER BY RAND()"""

    with conn.cursor() as cur:
        cur.execute(sql)
    tag_project_list_db_result = cur.fetchall()

    print(tag_project_list_db_result)

    tag_project_list_json = {"projects":[]}
    for tag_project in tag_project_list_db_result:
        project_container = {
            "team_name":tag_project[0], 
            "team_member":tag_project[1], 
            "team_number":tag_project[2], 
            "hashtag_main":tag_project[3], 
            "hashtag_custom_a":tag_project[4], 
            "hashtag_custom_b":tag_project[5], 
            "hashtag_custom_c":tag_project[6],
        }

        tag_project_list_json["projects"].append(project_container)

    return jsonify(tag_project_list_json)

@app.route('/project/<int:id>')
def project(id):
    Project =lfmodules.getProjects(id)
    title = Project[0][0]
    body = Project[0][10]
    return lfmodules.template(lfmodules.getContents(), f'<h2>{title}</h2>{body}')

@app.route('/project/<int:pj_id>/like')
def like_project(pj_id):
    conn = pymysql.connect(host=os.environ.get('DB_URL'),
                       user=os.environ.get('DB_USER'),
                       password=os.environ.get('DB_PASSWORD'),
                       db=os.environ.get('DB_NAME'),
                       charset='utf8')
    likesql = f"""SELECT 1 FROM like_table WHERE project_id = {pj_id} AND user_id = {session['User_id']}"""
    with conn.cursor() as cur:
        cur.execute(likesql)
    like_button = cur.fetchall()
    like_button = like_button[0][0]
    
    if like_button == 1:
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
            conn.commit()
        print(like_data[0][0])    
        like_button = 1
        return jsonify({"like_cnt": like_data[0][0]})
    
    else :
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
            conn.commit()
        print(like_data[0][0])    
        like_button = 0
        return jsonify({"like_cnt": like_data[0][0]})
    


@app.route('/logout')
def logout():
    session.pop('User_name', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)