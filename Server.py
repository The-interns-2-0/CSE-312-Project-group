from flask import Flask,make_response,request,redirect,abort
from pymongo import MongoClient
from json import dumps,loads
import bcrypt
import uuid
app = Flask(__name__)

mongo_client = MongoClient("mongo")
db = mongo_client['user_database']
collection = db['user_infor']


@app.route("/", methods=['GET','POST'])
def index():
    # if request.method == 'GET':
        print("here")
        with open("./public/index.html","r") as file:
            file = file.read()
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
    # print(request)
    data = request.form
    if data.get("reg_pass")!= data.get("conform_pass"):
        return abort(404)
    def hash_password(password):
        salt = bcrypt.gensalt()  
        return bcrypt.hashpw(password.encode(), salt)  
    collection.insert_one({"username":data.get("reg_user"),"password":hash_password(data.get("reg_pass")),"auth":""})

    return redirect("/",302)
    
if __name__ == '__main__':
    #port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=8080,debug=True)#debug=True

