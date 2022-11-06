from flask import Flask, request, redirect, jsonify, session, url_for, app
from dotenv import load_dotenv
from markupsafe import escape
import os
import pymysql
from datetime import timedelta
import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = 'secretkey'
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=60)

conn = pymysql.connect(host=os.environ.get('DB_URL'),
                       user=os.environ.get('DB_USER'),
                       password=os.environ.get('DB_PASSWORD'),
                       db=os.environ.get('DB_NAME'),
                       charset='utf8')

sql = "INSERT INTO user (user_name, user_student_number, user_major, user_login_time) VALUES (%s, %s, %s, %s)"

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

@app.route('/')
def index():
    if 'User_name' in session:
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
        Student_ID = request.form['Student_ID']
        User_name = request.form['User_name']
        User_major = request.form['User_major']
        User_login_time = datetime.datetime.now()
        session['User_name'] = request.form['User_name']
        
        with conn.cursor() as cur:
            cur.execute(sql, (User_name, Student_ID, User_major, User_login_time))
        conn.commit()
        return redirect(url_for('index'))

@app.route('/tag/')
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

@app.route('/class')
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

@app.route('/logout')
def logout():
    session.pop('User_name', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)