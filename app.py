from flask import Flask,jsonify,render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import pymongo
import bcrypt
import base64
import os,json

app=Flask(__name__)
app.secret_key = 'mysecret'

app.config['MONGO_DBNAME'] = 'SIH'
app.config['MONGO_URI'] = "mongodb+srv://bc007:msdhoni007@cluster0.dcb5w.mongodb.net/users?retryWrites=true&w=majority"

mongo = PyMongo(app)

@app.route('/login',methods=['POST'])
def login():
    data = request.json
    users = mongo.db.users
    login_user = users.find_one({"name": data["username"]})
    if login_user is not None:
        if bcrypt.hashpw(data["password"].encode('utf-8'), login_user["password"]) == login_user["password"]    :
            session["username"] = data["username"]
            return "Login Successfully"
    return "Invalid password",500
@app.route('/logout',methods=['GET'])
def logout():
    if session["username"] is not None:
        session["username"] = None
        return "Logout successfully"
    return "please login",500
@app.route('/register',methods=['POST'])
def register():
    data=request.json
    users = mongo.db.users
    curr_user=users.find_one({'name' : data['username']})
    if curr_user is None:
        hashpass = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt())
        users.insert({'name' : data['username'], 'password': hashpass})
        session['username'] = data['username']  
        return "Registered Succesfully"
    return "Username is already there",500
@app.route('/')
def hello():
    return "Welcome"
@app.route('/all',methods=['GET'])
def getAll():
    if session["username"] is not None:
        encoded = {}
        for direct in os.listdir('assets'):
            temp=[]
            for file in os.listdir('assets/'+direct):
                with open("assets/"+ direct + "/" + file,"rb") as img_file:
                    encoded_string= base64.b64encode(img_file.read())
                    out = encoded_string.decode('utf-8')
                temp.append(out)
            encoded[direct] = temp    
        post = json.dumps(encoded)
        return post
    return "please Login",500
if __name__=="__main__":
    app.run(debug=True)