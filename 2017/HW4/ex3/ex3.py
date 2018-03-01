#!/usr/bin/env python3
import os
import sys
import populate
from flask import g
from flask import Flask, current_app
from flask import render_template, request, jsonify
import pymysql


app = Flask(__name__)
username = "root"
password = "root"
database = "hw4_ex3"

## This method returns a list of messages in a json format such as
## [
##  { "name": <name>, "message": <message> },
##  { "name": <name>, "message": <message> },
##  ...
## ]
## If this is a POST request and there is a parameter "name" given, then only
## messages of the given name should be returned.
## If the POST parameter is invalid, then the response code must be 500.
@app.route("/messages",methods=["GET","POST"])
def messages():
    content = request.json
    # print(content)
    with db.cursor() as cursor:
        ## your code here

        if request.method == 'POST':
            form_param = request.form['name']
            input_param = request.args.get('name')

            if (content and 'name' in content):
                input_param = content['name']
                spl = input_param.split()
                if len(spl)>1:
                    return jsonify({}),500
                else:
                    name = spl[0]

                cmd = "SELECT name, message FROM messages WHERE name = %s;"
                cursor.execute(cmd, (name, ))
                tuples = cursor.fetchall()
                json_list = []
                for entry in tuples:
                    json_list.append({"name": entry[0], "message": entry[1]})
                # print(json_list)
                return jsonify(json_list),200
            elif input_param:
                spl = input_param.split()
                if len(spl)>1:
                    return jsonify({}),500
                else:
                    username = spl[0]

                cmd = "SELECT name, message FROM messages WHERE name = %s;"
                cursor.execute(cmd, (username, ))
                tuples = cursor.fetchall()
                json_list = []
                for entry in tuples:
                    json_list.append({"name": entry[0], "message": entry[1]})
                # print(json_list)
                return jsonify(json_list),200
            elif form_param:
                username = form_param

                cmd = "SELECT name, message FROM messages WHERE name = %s;"
                cursor.execute(cmd, (username, ))
                tuples = cursor.fetchall()
                json_list = []
                for entry in tuples:
                    json_list.append({"name": entry[0], "message": entry[1]})
                # print(json_list)
                return jsonify(json_list),200
            else:
                # cmd = "SELECT name, message FROM messages;"
                # cursor.execute(cmd)
                # tuples = cursor.fetchall()
                # json_list = []
                # for entry in tuples:
                #     json_list.append({"name": entry[0], "message": entry[1]})
                # return jsonify(json_list),200
                return jsonify({}), 500
        elif request.method == 'GET':
            cursor.execute("SELECT name, message FROM messages;")
            tuples = cursor.fetchall()
            json_list = []
            for entry in tuples:
                json_list.append({"name": entry[0], "message": entry[1]})
            # print(json_list)
            return jsonify(json_list),200


## This method returns the list of users in a json format such as
## { "users": [ <user1>, <user2>, ... ] }
## This methods should limit the number of users if a GET URL parameter is given
## named limit. For example, /users?limit=4 should only return the first four
## users.
## If the paramer given is invalid, then the response code must be 500.
@app.route("/users",methods=["GET"])
def contact():
    with db.cursor() as cursor:
        input_param = request.args.get('limit')
        if input_param:
            print(input_param)
            spl = input_param.split()
            if len(spl)>1:
                return jsonify({}),500
            else:
                limit = spl[0]

            cmd = "SELECT name FROM users limit %s;"
            # print(cmd, (int(limit), ))
            cursor.execute(cmd, (int(limit), ))
            tuples = cursor.fetchall()
            json = {"users": []}
            for entry in tuples:
                json["users"] += [entry[0]]
            # print(json)
            return jsonify(json),200
        else:
            cursor.execute("SELECT name FROM users;")
            tuples = cursor.fetchall()
            json = {"users": []}
            for entry in tuples:
                json["users"] += [entry[0]]
            # print(json)
            return jsonify(json),200

if __name__ == "__main__":
    seed = "randomseed"
    if len(sys.argv) == 2:
        seed = sys.argv[1]

    db = pymysql.connect("localhost",
                username,
                password,
                database)
    with db.cursor() as cursor:
        populate.populate_db(seed,cursor)
        db.commit()
    print("[+] database populated")

    app.run(host='0.0.0.0',port=80)
