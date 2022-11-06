from flask import Flask, request, redirect
from dotenv import load_dotenv
import os
import pymysql
import datetime

load_dotenv()

conn = pymysql.connect(host=os.environ.get('DB_URL'),
                       user=os.environ.get('DB_USER'),
                       password=os.environ.get('DB_PASSWORD'),
                       db=os.environ.get('DB_NAME'),
                       charset='utf8')

sql = "INSERT INTO user (user_name, user_student_number, user_major, user_login_time) VALUES (%s, %s, %s, %s)"

app = Flask(__name__)

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
                <li><a href="/create/">입장하기</a></li>
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

def getClassContents(class_name):
    ClassContents = f"""
                   SELECT *
                   FROM project
                   WHERE class_name = {class_name}
                   ORDER BY RAND()
                   """
    with conn.cursor() as cur:
            cur.execute(ClassContents)
            class_data = cur.fetchall()
    return class_data

@app.route('/')
def index():
    return template(getContents(), '<h2>Welcome to 2022 Learning Fair</h2>')
 

@app.route('/tag_test/')
def test():
    tag = request.args.get('tag')
    return tag

@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET': 
        content = '''
            <form action="/create/" method="POST">
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
        
        with conn.cursor() as cur:
            cur.execute(sql, (User_name, Student_ID, User_major, User_login_time))
        conn.commit()
        url = '/'
        return redirect(url)

@app.route('/tag_board/')
def tag_board():
    tag = request.args.get('tag')
    if tag == None :
        content = '''
        <form action="/tag_board/">
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

@app.route('/class_board/')
def class_board():
    class_num = request.args.get('class')
    if class_num == None :
        content = '''
        <form action="/class_board/">
        <ol>
        <li><a href="?class=1">I1</a></li>
        <li><a href="?class=2">I2</a></li>
        <li><a href="?class=3">I3</a></li>
        </ol>
        </form>
        '''
        return template(getContents(), content)
    else :
        content = f'''
        <h1>class가 {class_num}인 경우 데이터임.</h1>
        '''
        return templates(getClassContents(class_num), content)


if __name__ == '__main__':
    app.run(debug=True)