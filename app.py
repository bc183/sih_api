from flask import Flask,jsonify
import base64
import os,json

app=Flask(__name__)

@app.route('/')
def hello():
    return "Welcome"
@app.route('/all',methods=['GET'])
def getAll():
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
    return jsonify(post)

if __name__=="__main__":
    app.run(debug=True)