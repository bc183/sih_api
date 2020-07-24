from flask import Flask,jsonify
import base64
import os,json

app=Flask(__name__)

@app.route('/')
def hello():
    return "Welcome"
@app.route('/mouth',methods=['GET'])
def mouth():
    encoded = {}
    run={
        "message" : "IamRuning"
    }
    for file in os.listdir('env/assets/mouth'):
        with open('env/assets/mouth/'+file,"rb") as img_file:
            encoded_string= base64.b64encode(img_file.read())
            out = encoded_string.decode('utf-8')
        encoded[file] = out
        decode = base64.b64decode(out)
        filename='demo.jpg'
        with open(filename,"wb") as f:
            f.write(decode)
    post = json.dumps(encoded)
    return jsonify(post)

if __name__=="__main__":
    app.run(debug=True)