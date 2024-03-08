from flask import Flask
from pymongo import MongoClient
app = Flask(__name__)
 

try:

    mongo_client = MongoClient("mongo")
    db = mongo_client['user_atabase']
    collection = db['user_infor']

except Exception as erro:
    print("error in connecting to the Database")




@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

