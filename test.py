from flask import Flask, request, redirect
from sqlalchemy import create_engine, text 
 
app = Flask(__name__)
app.config.from_pyfile('config.py')

database = create_engine(app.config['DB_URL'], encoding = 'utf-8')
app.database = database
 
 
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
 
 
@app.route('/read/<int:id>/')
def read(id):
    title = ''
    body = ''
    for User in Users:
        if id == User['id']:
            title = User['User_name']
            body = User['Student_ID']
            break
    return template(getContents(), f'<h2>{title}</h2>{body}')
 
 
@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET': 
        content = '''
            <form action="/create/" method="POST">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit" value="create"></p>
            </form>
        '''
        return template(getContents(), content)
    elif request.method == 'POST':
        global nextId
        title = request.form['title']
        body = request.form['body']
        newUser = {'id': nextId, 'Student_ID': title, 'User_name': body}
        Users.append(newUser)
        url = '/'
        nextId = nextId + 1
        return redirect(url)
 
 
if __name__ == "__main__":
    app.run(debug=True)