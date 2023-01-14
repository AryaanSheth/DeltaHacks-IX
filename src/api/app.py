from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from random import randint as r

curdir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)


@app.route('/create', methods=['POST', 'GET'])
def Signup() -> str:
    # sample url: http://localhost:8080/create?username=hello&email=hello&password=1234
    
    # get the data from the url query
    uuid = r(1, 1000000)
    username = request.args.get('username')
    email = request.args.get('email')
    password = request.args.get('password')
    
    try:
        # connect to the database
        conn = sqlite3.connect('src/database/users.db')
        c = conn.cursor()
        
        # check if the username already exists in the database or not
        if c.execute("SELECT * FROM users WHERE Name = ?", (username,)).fetchone() is not None:
            return jsonify({
                'status': 402, 
                'info':username + " Already Exists",
                'data': 
                    {
                        'uuid': uuid, 
                        'username': username, 
                        'email': email, 
                        'password': password
                    }
                })
        

        # insert the data into the database
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (uuid, username, email, password, None, None))
        conn.commit()
        conn.close()
        
        # return a json object that has status code and the data added to the database
        return jsonify({
            'status': 200, 
            'info':'ok' ,'data': 
                {
                    'uuid': uuid, 
                    'username': username, 
                    'email': email, 
                    'password': password
                }
            })
    except:
        return jsonify({
            'status': 401, 
            'info':'err' ,'data': 
                {
                    'uuid': uuid, 
                    'username': username, 
                    'email': email, 
                    'password': password
                }
            })
    

@app.route('/login', methods=['POST', 'GET'])
def Login() -> str:
    # sample url: http://localhost:8080/login?username=hello&password=1234
    
    # get the data from the url query
    username = request.args.get('username')
    password = request.args.get('password')
    
    try:
        # connect to the database
        conn = sqlite3.connect('src/database/users.db')
        c = conn.cursor()

        # get the data from the database
        c.execute("SELECT * FROM users WHERE Name = ? AND Password = ?", (username, password))
        data = c.fetchone()
        conn.close()
        
        # return a json object that has status code and the data added to the database
        return jsonify({
            'status': 200, 
            'info':'ok' ,'data': 
                {
                    'uuid': data[0], 
                    'username': data[1], 
                    'email': data[2], 
                    'password': data[3]
                }
            })
    except:
            return jsonify({
                'status': 400, 
                'info':'User Not Found' ,'data': 
                    {
                        'uuid': 'null', 
                        'username': username, 
                        'email': 'null', 
                        'password': password
                    }
                })
            
            
@app.route('/addpfp', methods=['POST', 'GET'])
def AddPfp() -> str:
    # sample url: http://localhost:8080/addpfp?uuid=30863&url=https://google.com
    
    # get the data from the url query
    uuid = request.args.get('uuid')
    url = request.args.get('url')
    
    try:
        # connect to the database
        conn = sqlite3.connect('src/database/users.db')
        c = conn.cursor()
        
        # update the data in the database
        c.execute("UPDATE users SET Pfp = ? WHERE Uuid = ?", (url, uuid))
        conn.commit()
        conn.close()
        
        # return a json object that has status code and the data added to the database
        return jsonify({
            'status': 200, 
            'info':'ok' ,'data': 
                {
                    'uuid': uuid, 
                    'url': url
                }
            })
    except:
        return jsonify({
            'status': 400, 
            'info':'err' ,'data': 
                {
                    'uuid': uuid, 
                    'url': url
                }
            })
        
        

if __name__ == '__main__':
    app.run(port = 8080)