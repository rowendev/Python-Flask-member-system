# initial database
import email
import re
from urllib import request
import pymongo
import certifi
client = pymongo.MongoClient("mongodb+srv://root:root123@mycluster.9yv0f.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = client.member_system
print('*** database connection success ***')

#initial flask server
from flask import *
app = Flask(
    __name__,
    static_folder = 'public',
    static_url_path = '/'
)

app.secret_key = 'any string but secret'

# route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/member')
def member():
    if 'username' in session:
        print(session['username'])
        return render_template('member.html')
    else:
        return redirect('/')

@app.route('/signup', methods=['POST'])
def signup():
    # receive data from front-end
    username = request.form['username']
    email = request.form['useremail']
    password = request.form['password']
    if (username or email or password == ''):
        return redirect('/error?msg=請填寫完整資料')
    # handle data
    collection = db.user
    result = collection.find_one({
        'email':email
    })
    if result != None:
        return redirect('/error?msg=this email already exists')
    
    collection.insert_one({
        'username':username,
        'email':email,
        'password':password
    })
    return redirect('/')

@app.route('/signin', methods=['POST'])
def signin():
    email = request.form['useremail']
    password = request.form['password']
    collection = db.user
    result = collection.find_one({
        '$and':[
            {'email':email},
            {'password':password}
        ]
    })
    print('result:', result)
    if result == None:
        return redirect('/error?msg=帳號或密碼輸入錯誤')
    
    session['username'] = result['username']
    return redirect('/member')

@app.route('/signout')
def signout():
    del session['username']
    return redirect('/')
    
# /error?msg=error-message
@app.route('/error')
def error():
    message = request.args.get('msg', '發生錯誤,請聯繫客服')
    return render_template('error.html', message=message)

app.run(port=3000)

