from flask import Flask,make_response,request
from pymongo import MongoClient

app = Flask(__name__)
try:
    mongo_client = MongoClient("localhost")
    db = mongo_client['user_atabase']
    collection = db['user_infor']
except Exception as erro:
    print("error in connecting to the Database")

@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'GET':
        with open("./public/index.html","r") as file:
            file = file.read()
            response = make_response(file)
            response.headers['Content-Type'] = 'text/html; charset=utf-8'
            response.headers['X-Content-Type-Options'] = 'nosniff'
            return response
    else:
        data = request.json
        print(data)
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
@app.route("/register", methods=['POST'])
def get_data():
    # print(msg)
    data = request.json
    print(data)
    
    return "nothing"  
if __name__ == '__main__':
    app.run(host='localhost', port=8080,debug=True)#debug=True

