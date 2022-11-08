from flask import Flask, request, redirect, jsonify, session, url_for, app
from flask_cors import CORS
from dotenv import load_dotenv
from markupsafe import escape
import os
import pymysql
from datetime import timedelta
import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False
app.secret_key = 'secretkey'

conn = pymysql.connect(host=os.environ.get('DB_URL'),
                       user=os.environ.get('DB_USER'),
                       password=os.environ.get('DB_PASSWORD'),
                       db=os.environ.get('DB_NAME'),
                       charset='utf8')

sql = "INSERT INTO user (user_name, user_student_number, user_major, user_login_time, user_type) VALUES (%s, %s, %s, %s, %s)"
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

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)

@app.route('/')
def index():
    if 'User_name' in session:
        global like_button
        like_button = 0
        return '로그인 성공! 아이디는 %s' % escape(session['User_name']) + \
            "<br><a href = '/logout'>로그아웃</a>"

    return template(getContents(), '<h2>Welcome to 2022 Learning Fair</h2>')

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
        return template(getContents(), content)
    elif request.method == 'POST':
        #Student_ID = request.form['Student_ID']
        #User_name = request.form['User_name']
        #User_major = request.form['User_major']
        #User_login_time = datetime.datetime.now()
        #session['User_name'] = request.form['User_name']
        
        user_json = request.get_json()
        
        Student_ID = user_json['studentId']
        User_name = user_json['name']
        User_major = user_json['major']
        User_login_time = datetime.datetime.now()
        User_type = user_json['userType']

        session['User_name'] = user_json['name']


        with conn.cursor() as cur:
            cur.execute(sql, (User_name, Student_ID, User_major, User_login_time, User_type))
        conn.commit()
        #return redirect(url_for('index'))
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

@app.route('/project/<int:id>/')
def project(id):
    Project = getProjects(id)
    title = Project[0][0]
    body = Project[0][10]
    return template(getContents(), f'<h2>{title}</h2>{body}')

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