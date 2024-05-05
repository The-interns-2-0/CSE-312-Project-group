from flask import Flask,make_response,request,redirect,abort,jsonify
from pymongo import MongoClient
from json import dumps,loads
import bcrypt
import uuid
from html import escape
import hashlib
import os
from flask_socketio import SocketIO
from random import randrange
app = Flask(__name__)
socketio = SocketIO(app)

mongo_client = MongoClient("mongo")
# db = mongo_client['user_database']

# mongo_client = MongoClient("localhost")
player=[]
global gamenumber,left,right
gamenumber=-1
left=0
right=100
db = mongo_client["mongo-1"]
collection = db['user_infor']
auth_collection = db['auth_db']
chat_collection = db['chat']
LastWinner = db['winner']
private_collection=db['private']

like_collection=db["like_or_dislike"]
import time
ip_requests = {}
blocked_ips = {}
session_ids={}
@app.route("/", methods=['GET','POST'])
def index():
        client_ip = request.remote_addr
        print(ip_requests.get(client_ip))
        if  ip_requests.get(client_ip):
            ip_requests[client_ip] = {'count': ip_requests[client_ip].get("count")+5, 'times': time.time()}
        else:
            ip_requests[client_ip] = {'count': 5, 'times': time.time()}
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
            response.headers['Access-Control-Allow-Origin'] = '*'
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
        print(res)
        return res
    if request.method == 'POST':
        data = request.json
        msg=data.get("chat")
        msg=escape(msg)
        name = "Guest"
        token = request.cookies.get('auth_token')
        hashtoken = hashlib.sha256(str(token).encode()).hexdigest()
        id = uuid.uuid4()
        # print(hashtoken)
        if auth_collection.find_one({"auth_token":hashtoken})!= None:
            item = auth_collection.find_one({"auth_token":hashtoken})
            name = item["username"]
        user_info= collection.find_one({"username":name})
        profile_pic = "./public/Image/yogurt.jpg"
        if user_info != None:
            profile_pic = user_info["profile_pic"]
    
        chat_message = {
            "message": msg,
            "username": name,
            "_id" : str(id),
            "thumbsup":0,
            "thumbsdown":0,
            "profile_pic":profile_pic
        }
        chat_collection.insert_one(chat_message)

        response = make_response(({
            "message": msg,
            "username": name,
            "_id" : str(id),
            "thumbsup":0,
            "thumbsdown":0,
            "id" : str(id),
            "profile_pic":profile_pic
        }))
        # print(response)
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

@socketio.on('connect')
def handle_connection():
    freq={}
    for x in chat_collection.find({}):
      if x.get("username")!="Guest":
        freq[x.get("username")]=freq.get(x.get("username"),0)+1
    global session_ids
    auth=request.cookies.get('auth_token')
    if auth!=None and auth_collection.find_one({"auth_token":hashlib.sha256(str(auth).encode()).hexdigest()},{"_id":0})!=None:
        session_ids[request.sid] = auth_collection.find_one({"auth_token":hashlib.sha256(str(auth).encode()).hexdigest()},{"_id":0}).get("username")
    # print(freq)

    sorted_items = sorted(freq.items(), key=lambda item: item[1], reverse=True)[:3]

    # Create a new dictionary with keys as "first", "second", and "third"
    result_dict = {}
    for i, (key, value) in enumerate(sorted_items):
        result_dict[i + 1] = key
    # print(result_dict)
    socketio.emit('lead', result_dict)

@socketio.on('start')
def handle_start():
    if request.sid not in session_ids:
        socketio.emit('guesterror',room=request.sid)
        return
    if not player:
        global gamenumber
        gamenumber=randrange(0,100)
    users=[]
    print(player)
    print(request.sid)
    for play in player:
        users.append(session_ids[play])
        socketio.emit('join', {"user":session_ids[request.sid]},room=play)
    result_dict={"left":left,"right":right,"users":users}
    print(result_dict)
    socketio.emit('start', result_dict,room=request.sid)
    player.append(request.sid)
    socketio.emit('join', {"user":session_ids[request.sid]},room=request.sid)
    
@socketio.on('guess')
def handle_guess(data):
    print(data)
    guess=int(data.get("number"))
    ranges={}
    global left, right, gamenumber,player
    if guess < gamenumber:
        left = guess + 1
        ranges= {'left': left, 'right': right}
    elif guess > gamenumber:
        right = guess - 1
        ranges= {'left': left, 'right': right}
    else:

        # last_list = LastWinner.find({})
        
        if LastWinner.find_one({"player":"player"})== None:
            LastWinner.insert_one({"player": "player", "playerName": session_ids[request.sid]})
        else:
            # chat_collection.update_one({"_id":post_id},{"$set":{"thumbsup":chat_item["thumbsup"] + 1 }})
            LastWinner.update_one({"player": "player"}, {"$set":{ "playerName": session_ids[request.sid]}})

        socketio.emit('end',{"player":session_ids[request.sid]})
        
        #session_ids[request.sid] to database
        player=[]
        gamenumber=-1
        left=0
        right=100
    ranges["player"]=session_ids[request.sid]
    ranges["number"]=guess
    for play in player:
        socketio.emit('continue', ranges,room=play)


@socketio.on('message')
def handle_message(data):
    client_ip = request.remote_addr
    print(ip_requests[client_ip]['count'])
    if client_ip in blocked_ips:
        if time.time() - blocked_ips[client_ip] >= 30:
            del blocked_ips[client_ip] 
        else:
            socketio.emit('error','Too Many Requests. Please try again later.')
            return
    if client_ip in ip_requests:
        if ip_requests[client_ip]['times'] < time.time() - 10:
            ip_requests[client_ip] = {'count': 1, 'times': time.time()}
        else:
            ip_requests[client_ip]['count'] += 1
            if ip_requests[client_ip]['count'] > 50:
                blocked_ips[client_ip] = time.time() 
                socketio.emit('error', 'Too Many Requests. Please try again later.')
                return 
    else:
        ip_requests[client_ip] = {'count': 1, 'times': time.time()}
    msg=data.get("chat")
    msg=escape(msg)
    name = "Guest"
    token = request.cookies.get('auth_token')
    hashtoken = hashlib.sha256(str(token).encode()).hexdigest()
    id = uuid.uuid4()
    if auth_collection.find_one({"auth_token":hashtoken})!= None:
        item = auth_collection.find_one({"auth_token":hashtoken})
        # print(item)
        name = item["username"]
    user_info= collection.find_one({"username":name})
    profile_pic = "./public/Image/yogurt.jpg"
    if user_info != None:
        profile_pic = user_info.get("profile_pic",profile_pic)
        if profile_pic=="none":
            profile_pic= "./public/Image/yogurt.jpg"
    
    chat_message = {
        "message": msg,
        "username": name,
        "_id" : str(id),
        "thumbsup":0,
        "thumbsdown":0,
        "profile_pic":profile_pic
    }
    response = (({
            "message": msg,
            "username": name,
            "_id" : str(id),
            "thumbsup":0,
            "thumbsdown":0,
            "profile_pic":profile_pic
        }))
    delay=int(data.get("sec"))
    def post_scheduler( delay):
        while delay > 0:
            print(delay)
            delay_msg = {
                "message": delay,
                "username": name,
                "_id" : str(id),
                "thumbsup":0,
                "thumbsdown":0,
                "profile_pic":profile_pic
            }
            socketio.emit('response', delay_msg)
            delay -= 1
            socketio.sleep(1)
        chat_collection.insert_one(chat_message)
        socketio.emit('response', response)
    if delay>0:
        socketio.start_background_task(post_scheduler, delay)
    else:
        chat_collection.insert_one(chat_message)
        socketio.emit('response', response)  # Echo the message back to the client
    freq={}
    for x in chat_collection.find({}):
      if x.get("username")!="Guest":
        freq[x.get("username")]=freq.get(x.get("username"),0)+1
    # print(freq)

    sorted_items = sorted(freq.items(), key=lambda item: item[1], reverse=True)[:3]

    # Create a new dictionary with keys as "first", "second", and "third"
    result_dict = {}
    for i, (key, value) in enumerate(sorted_items):
        result_dict[i + 1] = key
    # print(result_dict)
    socketio.emit('lead', result_dict)

UPLOAD_FOLDER = './public/Image'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/upload-media", methods=['POST'])
def upload():
    #get auth_token 
    token = request.cookies.get('auth_token')
    hashtoken = hashlib.sha256(str(token).encode()).hexdigest()
    # Check if the user is authenticated
    if auth_collection.find_one({"auth_token": hashtoken}) is not None:
        if 'upload' not in request.files:
            return "No file part", 400
        file = request.files['upload']
        if file.filename == '':
            return "No selected file", 400 
        if file:
            filename =  file.filename
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            # Update the user's profile picture in the database
            item = auth_collection.find_one({"auth_token": hashtoken})
            #filename = "<img src=" + '"' +image_filename+ '" ' +  "class=" + '"'+ "m_image" +'"' +"/>"
            name = item["username"]
            collection.update_one({"username": name}, {"$set": {"profile_pic": "./public/Image/" + filename}})
            all_chat  = chat_collection.find({})
            # print("lokokokokokokkokokookook")
            for i in all_chat:
                # print("----------------OOOOOOOOOO--------")
                if i["username"] == name:
                    # chat_collection.update
                    chat_collection.update_one({"_id": i["_id"]}, {"$set": {"profile_pic": "./public/Image/" + filename}})
            return redirect("/",302)
    return 401


@app.route("/winner")
def winnerBegin():
    winner_document = LastWinner.find_one({})
    
    if winner_document:
        player_name = winner_document.get("playerName")
        if player_name:
            winner = {"name": player_name}
            return jsonify(winner)
    
    default_winner = {"name": "No winner yet"}
    return jsonify(default_winner)



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080,allow_unsafe_werkzeug=True)#, ssl_context=('./nginx/cert.pem', './nginx/private.key')
    # app.run(host='0.0.0.0', port=8080,debug=True,threaded=True)
