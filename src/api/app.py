from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from random import randint as r

curdir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)



# SQLIte3 Database for users collection      

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
        
        

@app.route('/addCourse', methods=['POST', 'GET'])
def AddCourse() -> str:
    # sample url: http://localhost:8080/addCourse?course=hello&uuid=30863
    
    # Since sqlite3 has no arrays we will store the courses in a string and then split it via a comma 
    # We will fetch a course via name from the courses table and then add it to the user's courses making sure to format it correctly
    
    course = request.args.get('course') + ','# course in courses table
    uuid = request.args.get('uuid') # user's uuid that will be added to the course
    
    conn = sqlite3.connect('src/database/users.db')
    c = conn.cursor()
    
    # fetch the course title from the courses table and store it in a variable
    cur = (c.execute("SELECT * FROM courses WHERE Name = ?", (course,)).fetchone()[0]).rstrip(",")
    
    # fetch all the courses from the user's courses and store it in a variable
    usrcourses = ((c.execute("SELECT * FROM users WHERE Uuid = ?", (uuid,)).fetchone()[5]).split(","))[:-1]
    
    print(cur, usrcourses)
    
    # chcek if the course already exists in the user's courses
    if cur in usrcourses:
        
        return jsonify({
            'status': 400, 
            'info':'Course Already Exists' ,
            'data': 
                {
                    'uuid': uuid, 
                    'course': course
                }
            })

    # add the course to the user's courses
    # c.execute("UPDATE users SET Courses = ? WHERE Uuid = ?", (cur, uuid))
    # conncateinate the course to the user's current courses and then update the database
    c.execute("UPDATE users SET Courses = ? || Courses WHERE Uuid = ?", ((cur+','), uuid))
    # concateinate the new course with a comma to the user
    
    conn.commit()
    conn.close()

    return jsonify({
        'status': 200, 
        'info':'ok' ,
        'data': 
            {
                'uuid': uuid, 
                'course': course
            }
        })
        
        
        
# SQLIte3 Database for courses collection        

@app.route('/addcourse', methods=['POST', 'GET'])
def addcourse() -> str:
    # sample url: http://localhost:8080/addcourse?title=hello&price=1234&author=hello&rating=5
    
    # users.db has a courses table in the form name price author rating. The name serves as a uuid and it unique. price is a real number, author is a string, and rating is a integer.
    
    title = request.args.get('title')
    price = request.args.get('price')
    author = request.args.get('author')
    rating = request.args.get('rating')
    
    try:
        conn=sqlite3.connect('src/database/users.db')
        c=conn.cursor()
        #c.execute("INSERT INTO courses VALUES (?, ?, ?, ?)", (title, price, author, rating))
        c.execute("INSERT INTO courses VALUES (?, ?, ?, ?)", (title + ",", price, author, rating))
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 200,
            'info': 'ok',
            'data': {
                'title': title,
                'price': price,
                'author': author,
                'rating': rating
            }
        })
        
    except:
        return jsonify({
            'status': 400,
            'info': 'err',
            'data': {
                'title': title,
                'price': price,
                'author': author,
                'rating': rating
            }
        })

    
    
    
        

if __name__ == '__main__':
    app.run(port = 8080)