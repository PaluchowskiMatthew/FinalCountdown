from flask import Flask
from flask import request
from flask import render_template
from flask import *
import base64
import json
import hmac
import datetime, time



app = Flask(__name__)

SECRET_KEY = 'IwQCAAdTCUseBUwUQwAaGhIFSTQKUAIDDgJI'.encode('utf-8')
COOKIE_VALUE = ''
IS_ADMIN = False

@app.route('/index')
def index():
    return 200;

@app.route('/ex3/login', methods=['POST'])
def login():
    error = None
    print(request.method)
    if request.method == 'POST':
        json_post = request.get_json()
        print(json_post)
        
        cookie = create_cookie(json_post)
        cookie_value = btoa(cookie)
        print(cookie_value)
        global COOKIE_VALUE
        COOKIE_VALUE = cookie_value
        
        redirect_to_index = redirect('/index')
        #     response = current_app.make_response(redirect_to_index )
        response = app.make_response('')  
        response.set_cookie('LoginCookie',value=cookie_value)
        return response
        
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)
    
def create_cookie(json_post):
    admin = {"user": "administrator", "pass": "42"}
    
    d = datetime.datetime.utcnow()
    for_js = int(time.mktime(d.timetuple())) * 1000
    
    cookie = json_post['user'] + ',' + str(for_js)
    
    global IS_ADMIN
    if json_post == admin:
        IS_ADMIN = True
        ending = ',com402,hw2,ex3,administrator,'
    else:
        IS_ADMIN = False
        ending = ',com402,hw2,ex3,user,'
        
    cookie += ending
    hmac_hex = hmac.new(SECRET_KEY, cookie.encode('utf-8')).hexdigest()
    cookie += hmac_hex
    return cookie
    
@app.route('/ex3/list', methods=['POST'])
def list():
    cookie_value = request.cookies.get('LoginCookie')
    
    print('cookie_value: ', str(cookie_value).encode('utf-8'))
    print('COOKIE_VALUE: ', str(COOKIE_VALUE).encode('utf-8'))
    print('IS_ADMIN: ', IS_ADMIN)
    
    if isinstance(cookie_value, str):
        cookie_value = str(cookie_value).encode('utf-8')
    

    
    if cookie_value == COOKIE_VALUE:
        if IS_ADMIN:
            return "", 200
        else:
            return "", 201
    else:
        return "", 403 


def btoa(s):
    if isinstance(s, str):
        return base64.b64encode(str.encode(s))
    elif isinstance(s, unicode):
        return base64.b64encode(s)
    


app.run()