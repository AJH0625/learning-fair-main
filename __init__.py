from flask import Flask, request, redirect
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
import pymysql

load_dotenv()

conn = pymysql.connect(host=os.environ.get('DB_URL'),
                       user=os.environ.get('DB_USER'),
                       password=os.environ.get('DB_PASSWORD'),
                       db=os.environ.get('DB_NAME'),
                       charset='utf8')

sql = "INSERT INTO user_test (user_test_name, uset_test_num) VALUES (%s, %d)"

app = Flask(__name__)
 

nextId = 4
Users = [
    {'id': 1, 'Student_ID': 2020311271, 'User_name': '장지원'},
    {'id': 2, 'Student_ID': 2018311068, 'User_name': '손승열'},
    {'id': 3, 'Student_ID': 2019312133, 'User_name': '차은우'}
]
 
 
def template(contents, content):
    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">2022 Learning Fair 방문자</a></h1>
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
 
 
def getContents():
    liTags = ''
    for User in Users:
        liTags = liTags + f'<li><h3>{User["Student_ID"]}</h3>{User["User_name"]}</li>'
    return liTags
 
 
@app.route('/')
def index():
    return template(getContents(), '<h2>Welcome to 2022 Learning Fair</h2>')
 
 
@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET': 
        content = '''
            <form action="/create/" method="POST">
                <p><input type="int" name="Student_ID" placeholder="Student_ID"></p>
                <p><input type="text" name="User_name" placeholder="User_name"></p>
                <p><input type="submit" value="로그인"></p>
            </form>
        '''
        return template(getContents(), content)
    elif request.method == 'POST':
        global nextId
        Student_ID = request.form['Student_ID']
        User_name = request.form['User_name']
        newUser = {'id': nextId, 'Student_ID': Student_ID, 'User_name': User_name}
        Users.append(newUser)
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (User_name, Student_ID))
                conn.commit()
        url = '/'
        nextId = nextId + 1
        return redirect(url)
 
if __name__ == "__main__":
    app.run(debug=True)