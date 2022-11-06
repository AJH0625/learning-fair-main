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
    return liTags
 
 
@app.route('/')
def index():
    return template(getContents(), '<h2>Welcome to 2022 Learning Fair</h2>')
 
 
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
 
if __name__ == '__main__':
    app.run(debug=True)