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
app.secret_key = 'secretkey'
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=60)

conn = pymysql.connect(host=os.environ.get('DB_URL'),
                       user=os.environ.get('DB_USER'),
                       password=os.environ.get('DB_PASSWORD'),
                       db=os.environ.get('DB_NAME'),
                       charset='utf8')

sql = "INSERT INTO user (user_name, user_student_number, user_major, user_login_time) VALUES (%s, %s, %s, %s)"
like_button = 0

def template(contents, content):
    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">2022 Learning Fair</a></h1>
            <ol>
                {contents}
            </ol>
            {content}
            <ul>
                <li><a href="/login">입장하기</a></li>
            </ul>
        </body>
    </html>
    '''

def templates(contents, content):
    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">2022 Learning Fair</a></h1>
            <ol>
                {contents}
            </ol>
            {content}
        </body>
    </html>
    '''
 
def getContents():
    liTags = ''
    return liTags

def getProjects(id):
    Projects = f"""
                SELECT *
                FROM project
                WHERE project_id = {id}
                """
    with conn.cursor() as cur:
        cur.execute(Projects)
        project_data = cur.fetchall()
    return project_data

def getTagContents(tag):
    TagContents = f"""
                   SELECT *
                   FROM project
                   WHERE hashtag_main = {tag}
                   ORDER BY RAND()
                   """
    with conn.cursor() as cur:
            cur.execute(TagContents)
            tag_data = cur.fetchall()
    return tag_data

def getUserID(user_token):
    getUsID = f"""
                SELECT user_id
                FROM user
                WHERE user_token = {user_token}
                """
    with conn.cursor() as cur:
            cur.execute(getUsID)
            user_data = cur.fetchall()
    return user_data[0][0]

def getClassContents(class_code):
    ClassContents = f"""
                   SELECT *
                   FROM project
                   WHERE class_name = {class_code}
                   ORDER BY RAND()
                   """
    with conn.cursor() as cur:
        cur.execute(ClassContents)
        class_data = cur.fetchall()
    return class_data

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
        Student_ID = request.form['Student_ID']
        User_name = request.form['User_name']
        User_major = request.form['User_major']
        User_login_time = datetime.datetime.now()
        session['User_name'] = request.form['User_name']
        
        with conn.cursor() as cur:
            cur.execute(sql, (User_name, Student_ID, User_major, User_login_time))
        conn.commit()
        
        User_token = secrets.token_hex(nbytes=32)
        sql2 = f"""SELECT user_id FROM user WHERE user_name = '{User_name}'"""

        with conn.cursor() as cur:
            cur.execute(sql2)
        user_id_db_result = cur.fetchall()

        print(user_id_db_result[0][0])

        session['User_token'] = User_token
        print(session['User_token'])
        print(session['User_name'])
        
        return redirect(url_for('index'))
        
@app.route('/testid')
def testid():
    us_id = getUserID(session['User_token'])
    print(us_id)
    return jsonify({"test":"hello"})


@app.route('/testjson')
def testjson():
    print(session['User_token'])
    return jsonify({"test":"hello"})

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
        return template(getContents(), content)
    else :
        content = f'''
        <h1>tag가 {tag}인 경우 데이터임.</h1>
        '''
        return templates(getTagContents(tag), content)

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
        return template(getContents(), content)
    else :
        content = f'''
        <h1>class가 {class_code}인 경우 데이터임.</h1>
        '''
        return templates(getClassContents(class_code), content)

@app.route('/project/<int:id>')
def project(id):
    Project = getProjects(id)
    title = Project[0][0]
    body = Project[0][10]
    return template(getContents(), f'<h2>{title}</h2>{body}')

@app.route('/session-check', methods=['POST'])
def session_check():
    print(session)

    session_check_json = request.get_json()

    if session_check_json['token'] in session:
        return jsonify({"session":"active"})
    else:
        return jsonify({"session":"deactive"})

@app.route('/project/<int:pj_id>/like')
def likes_project(pj_id):
    us_id = getUserID(session['User_token'])
    conn = pymysql.connect(host=os.environ.get('DB_URL'),
                       user=os.environ.get('DB_USER'),
                       password=os.environ.get('DB_PASSWORD'),
                       db=os.environ.get('DB_NAME'),
                       charset='utf8')
    likesql = f"""SELECT EXISTS(SELECT * FROM like_table WHERE project_id == {pj_id} AND user_id == {us_id}) AS t"""
    conn.cursor.execute(likesql)
    like_button = conn.cursor.fetchall()
    like_button = like_button[0][0]
    print(like_button)
    return like_button

@app.route('/projects/<int:pj_id>/like')
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
        print(like_data[0][0], '\n') 
        print(session['User_name'])
        print('님이 좋아요를 눌렀어요')   
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

if __name__ == "__main__":
    app.run(debug=True)