from flask import Flask,make_response,request,redirect, url_for
from pymongo import MongoClient
from json import dumps,loads
app = Flask(__name__)

mongo_client = MongoClient("localhost")
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
    # else:
    #     data = request.json
    #     print(data["user"])
    # with open("./public/index.html","r") as file:
    #         file = file.read()
    #         response = make_response(file)
    #         response.headers['Content-Type'] = 'text/html; charset=utf-8'
    #         response.headers['X-Content-Type-Options'] = 'nosniff'
    #         return response
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
    data = request.json
    data.get("reg_user")
    data.get("reg_pass")
    return redirect("/favicon.ico",302)
    
if __name__ == '__main__':
    app.run(host='localhost', port=8080,debug=True)#debug=True

