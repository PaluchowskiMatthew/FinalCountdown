from flask import Flask
from flask import request
from flask import render_template
import base64
import json


app = Flask(__name__)

@app.route('/hw2/ex1', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        json_post = request.get_json()
        username = json_post["user"]
        password = json_post["pass"]
        if valid_login(username, password): #valid_login(str(request.form['username']), str(request.form['password'])):
            return "", 200 # json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
        else:
            error = 'Invalid username/password'
            return "", 400 #json.dumps({'success':False}), 400, {'ContentType':'application/json'} 
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)
    
    
def valid_login(username, password):
    mySecureOneTimePad = "Never send a human to do a machine's job";
    
    # if (len(username) > 100):
    #     return False
    # elif (len(password) > 100):
    #     return False
    
    enc = superencryption(username, mySecureOneTimePad).decode("utf-8")
    
    if (enc != password):
        print('invalid')
        return False
    else:
        print('valid')
        return True
    
def ascii(a):
    return ord(a[0])

def toChar(i):
    return chr(i)
    
def btoa(s):
    return base64.b64encode(str.encode(s))

def superencryption(msg, key):
    if(len(key) < len(msg)):
        diff = len(msg) - len(key)
        key += key[0:diff]
    
    amsg = [ascii(m) for m in list(msg)]
    akey = [ascii(m) for m in list(key[0:len(msg)]) ]
    
    encr = ""
    for i, m in enumerate(amsg):
        encr += toChar(m ^ akey[i])
    return btoa(encr)

app.run()