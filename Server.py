from flask import Flask,make_response,request,redirect,abort,jsonify
from pymongo import MongoClient
from json import dumps,loads
import bcrypt
import uuid
from html import escape
import hashlib

app = Flask(__name__)

mongo_client = MongoClient("mongo")
db = mongo_client['user_database']
collection = db['user_infor']
auth_collection = db['auth_db']
chat_collection = db['chat']
@app.route("/", methods=['GET','POST'])
def index():
    # if request.method == 'GET':
        with open("./public/index.html","r") as file:
            file = file.read()
            auth=request.cookies.get('auth_token')
            # print(hashlib.sha256(str(auth).encode()).hexdigest())
            # print(auth_collection.find_one({"auth_token":hashlib.sha256(str(auth).encode()).hexdigest()},{"_id":0}))
            if auth!=None and auth_collection.find_one({"auth_token":hashlib.sha256(str(auth).encode()).hexdigest()},{"_id":0})!=None:
                file=file.replace("Guest",auth_collection.find_one({"auth_token":hashlib.sha256(str(auth).encode()).hexdigest()},{"_id":0}).get("username"))
            response = make_response(file)
            response.headers['Content-Type'] = 'text/html; charset=utf-8'
            response.headers['X-Content-Type-Options'] = 'nosniff'
            return response

@app.route("/functions.js")
def func():
    with open("./public/function.js","r") as file:
        file = file.read()
        response = make_response(file)
        response.headers['Content-Type'] = 'text/javascript; charset=utf-8'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
@app.route("/style.css")
def style():
    with open("./public/style.css","r") as file:
        file = file.read()
        response = make_response(file)
        response.headers['Content-Type'] = 'text/css; charset=utf-8'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
@app.route("/favicon.ico")
def fav():
    with open("./public/style.css","r") as file:
        file = file.read()
        response = make_response(file)
        response.headers['Content-Type'] = 'text/css; charset=utf-8'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
@app.route("/register", methods=['GET','POST'])

def get_data():
    data = request.form
    # print("heres")
    print(data)
    if collection.find_one({"username":escape(data.get("reg_user"))})!=None:
        print("colle")
        return abort(404)
    if data.get("reg_pass")!= data.get("conform_pass"):
        print("pass")
        return abort(404)
    def hash_password(password):
        salt = bcrypt.gensalt()  
        return bcrypt.hashpw(password.encode(), salt)  
    collection.insert_one({"username":escape(data.get("reg_user")),"password":hash_password(data.get("reg_pass")),"auth":""})
    return redirect("/",302)
@app.route("/login", methods=['GET','POST'])
def login():
    data = request.form
    thisitem = collection.find_one({"username":data.get("login_user")})

    if bcrypt.checkpw(data.get("login_passs").encode(),thisitem["password"]) == True:

        auth_token = uuid.uuid4()
        hashtoken = hashlib.sha256(str(auth_token).encode()).hexdigest()
        response = make_response(redirect('/',302))
        response.set_cookie('auth_token', str(auth_token),3600,httponly=True)
        response.headers['HttpOnly']='True'
        auth_collection.delete_one({"username":data.get("login_user")})
        auth_collection.insert_one({"username":data.get("login_user"),"auth_token":hashtoken})
        return response
    return abort(404)
@app.route("/logout", methods=['GET','POST'])
def logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie('auth_token')
    return resp
@app.route("/addchat", methods=['GET','POST'])
def add():
    if request.method == 'GET':
        chat=list(chat_collection.find({},{"_id":0}))
        # print(chat)
        res=dumps(chat)
        return res
    if request.method == 'POST':
        data = request.json
        msg=data.get("chat")
        print(msg)
        msg=escape(msg)
        auth=request.cookies.get('auth_token')

        None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080,debug=True)#debug=True

