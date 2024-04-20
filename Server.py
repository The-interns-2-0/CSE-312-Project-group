from flask import Flask,make_response,request,redirect,abort,jsonify
from pymongo import MongoClient
from json import dumps,loads
import bcrypt
import uuid
from html import escape
import hashlib
import os

app = Flask(__name__)

# mongo_client = MongoClient("mongo")
# db = mongo_client['user_database']

mongo_client = MongoClient("mongodb://cse-312-project-group-mongo-1")
db = mongo_client["mongo-1"]
collection = db['user_infor']
auth_collection = db['auth_db']
chat_collection = db['chat']


#data base for like and dislikes
like_collection=db["like_or_dislike"]
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
    




@app.route("/public/Image/<filename>")
def serve_image(filename):
    image_path = os.path.join("./public/Image", filename)
    if os.path.exists(image_path):
        with open(image_path, "rb") as file:
            file_content = file.read()
        response = make_response(file_content)
        response.headers['Content-Type'] = 'image/jpeg'
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
    #collection.insert_one({"username":escape(data.get("reg_user")),"password":hash_password(data.get("reg_pass"))})

    #profile pic field
    collection.insert_one({"username":escape(data.get("reg_user")),"password":hash_password(data.get("reg_pass")),"profile_pic":"none"})
    return redirect("/",302)


@app.route("/login", methods=['GET','POST'])
def login():
    data = request.form
    thisitem = collection.find_one({"username":data.get("login_user")})
    if thisitem==None:
        return abort(404)
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
        chat=list(chat_collection.find({}))
        res=dumps(chat)
        return res
    if request.method == 'POST':
        data = request.json
        msg=data.get("chat")
        msg=escape(msg)
        name = "Guest"
        token = request.cookies.get('auth_token')
        hashtoken = hashlib.sha256(str(token).encode()).hexdigest()
        id = uuid.uuid4()
        if auth_collection.find_one({"auth_token":hashtoken})!= None:
            item = auth_collection.find_one({"auth_token":hashtoken})
            name = item["username"]
        chat_message = {
            "message": msg,
            "username": name,
            "_id" : str(id),
            "thumbsup":0,
            "thumbsdown":0
        }
        chat_collection.insert_one(chat_message)
        

        response = make_response(jsonify({
            "message": msg,
            "username": name,
            "_id" : str(id),
            "thumbsup":0,
            "thumbsdown":0,
            "id" : str(id)
        }))
        response.status_code = 201
        return response

@app.route("/like", methods=['GET','POST'])
def like():
    data = request.json
    post_id = data.get("id")
    token = request.cookies.get('auth_token')
    # print(token)
    hashtoken = hashlib.sha256(str(token).encode()).hexdigest()
    name = "Guest"
    if auth_collection.find_one({"auth_token":hashtoken})!= None:
        item = auth_collection.find_one({"auth_token":hashtoken})
        chat_item = chat_collection.find_one({"_id":post_id})
        name = item["username"]
    if like_collection.find_one({"User":name,"Post_id":post_id})==None:
        chat_collection.update_one({"_id":post_id},{"$set":{"thumbsup":chat_item["thumbsup"] + 1 }})
        like_collection.insert_one({"Post_id":post_id,"LorD":"like","User":name})
    response = make_response(jsonify({
            "Post_id":post_id,
            "LorD":"like",
            "User":name,
        }))
    response.status_code = 201
    return response 


@app.route("/dislike", methods=['GET','POST'])
def dislike():
    data = request.json
    post_id = data.get("id")
    token = request.cookies.get('auth_token')
    # print(token)
    hashtoken = hashlib.sha256(str(token).encode()).hexdigest()
    name = "Guest"
    if auth_collection.find_one({"auth_token":hashtoken})!= None:
        item = auth_collection.find_one({"auth_token":hashtoken})
        chat_item = chat_collection.find_one({"_id":post_id})
        name = item["username"]
    if like_collection.find_one({"User":name,"Post_id":post_id})==None:
        chat_collection.update_one({"_id":post_id},{"$set":{"thumbsdown":chat_item["thumbsdown"] + 1 }})
        like_collection.insert_one({"Post_id":post_id,"LorD":"like","User":name})
    response = make_response(jsonify({
            "Post_id":post_id,
            "LorD":"like",
            "User":name,
        }))
    response.status_code = 201
    return response 

#Create the path where new uploaded image is saved.
UPLOAD_FOLDER = './public/Image'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route("/media-upload", method = ['GET','POST'])
# def upload():
#     #get auth_token 
#     token = request.cookies.get('auth_token')
#     hashtoken = hashlib.sha256(str(token).encode()).hexdigest()

#     #uploading process
#     file = request.files['upload']
#     #img_name = "img" + str(uuid.uuid4())
#     path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#     file.save(path)
#     if auth_collection.find_one({"auth_token":hashtoken})!= None:
#         item = auth_collection.find_one({"auth_token":hashtoken})
#         collection.update_one({"auth_token":hashtoken},{"$set":{"profile_pic":file.filename }})
#         name = item["username"]
#     return path


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080,debug=True)#debug=True
