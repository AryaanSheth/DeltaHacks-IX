from flask import Flask, request, jsonify
import sqlite3
import os
from random import randint as r
from flask_cors import CORS

curdir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
CORS(app)

#NOTE - Status 400 means something went wrong, Status 200 means everything went well. Refer to info endpoint for more info on error 


# root
@app.route('/', methods=['POST', 'GET'])
def ping() -> str:
    return jsonify({
        'status': 200, 
        'info':'ok' ,'data': 
            {
                'uuid': 'null', 
                'username': 'null', 
                'email': 'null', 
                'password': 'null'
            }
        })


# SQLIte3 Database for users collection      

@app.route('/createusr', methods=['POST', 'GET'])
def Signup() -> str:
    # sample url: http://localhost:8080/createusr?username=hello&email=hello&password=1234
    
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
                'status': 400, 
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
        # just in case something goes wrong
        return jsonify({
            'status': 400, 
            'info':'err' ,'data': 
                {
                    'uuid': uuid, 
                    'username': username, 
                    'email': email, 
                    'password': password
                }
            })
    

@app.route('/loginusr', methods=['POST', 'GET'])
def Login() -> str:
    # sample url: http://localhost:8080/loginusr?username=hello&password=1234
    
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
        # just in case something goes wrong
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
    
    # connect to the database
    conn = sqlite3.connect('src/database/users.db')
    c = conn.cursor()
    

    # check if the username already exists in the database or not
    if c.execute("SELECT * FROM users WHERE Uuid = ?", (uuid,)).fetchone() is None:
        return jsonify({
            'status': 400, 
            'info':'User Not Found',
            'data': 
                {
                    'uuid': uuid, 
                    'url': url
                }
            })
    
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
        

@app.route('/addcourseusr', methods=['POST', 'GET'])
def AddCourse() -> str:
    # link http://localhost:8080/addcourseusr?uuid=30863&course=math
    
    # the users courses are stored in a string in the database where each individual course is separated by a comma
    # "course1,course2,course3," <- this is how the courses are stored in the database
    # To add a course we get a course query. If the users current courses is empty we can just add the course to the database followed by a comma
    # If the user already has courses we can just add the new course to the end of the string followed by a comma and then update the database
    # making sure that the course is not already in the database for the user
    
    uuid = request.args.get('uuid')
    course = request.args.get('course')
    
    # connect to the database
    conn = sqlite3.connect('src/database/users.db')
    c = conn.cursor()
    
    try:
        # search the courses table to see if an existing course has the same name as the course+"," that we are trying to add
        if c.execute("SELECT * FROM courses WHERE Name = ?", (course + ",",)).fetchone() is None:
            # if the course does not exist throw an error
            return jsonify({
                'status': 400,
                'info': 'Course Not Found',
                'data':
                    {
                        'uuid': uuid,
                        'course': course
                    }
                })
        
        # check if the username has any courses 
        if c.execute("SELECT * FROM users WHERE Uuid = ?", (uuid,)).fetchone()[5] is None:
            # if the user has no courses we can just add the course to the database
            c.execute("UPDATE users SET Courses = ? WHERE Uuid = ?", (course + ",", uuid))
            conn.commit()
            conn.close()
            
            # return a json object that has status code and the data added to the database
            return jsonify({
                'status': 200, 
                'info':'ok' ,'data': 
                    {
                        'uuid': uuid, 
                        'course': course
                    }
                })
        else:
            # this happens if the user already has courses
            # check if this course is already in the database
            if course in c.execute("SELECT * FROM users WHERE Uuid = ?", (uuid,)).fetchone()[5].split(",")[:-1]:
                return jsonify({
                    'status': 400, 
                    'info':'Course Already Exists' ,'data': 
                        {
                            'uuid': uuid, 
                            'course': course
                        }
                    })
            else:
                # this happens when the course is not in the database for the user we can add it to the database
                c.execute("UPDATE users SET Courses = ? WHERE Uuid = ?", (c.execute("SELECT * FROM users WHERE Uuid = ?", (uuid,)).fetchone()[5] + course + ",", uuid))
                
                conn.commit()
                conn.close()

                # return a json object that has status code and the data added to the database
                return jsonify({
                    'status': 200,
                    'info':'ok' ,'data':
                        {
                            'uuid': uuid,
                            'course': course
                        }
                    })

    except:
        return jsonify({
            'status': 400,
            'info': 'User Not Found',
            'data':
                {
                    'uuid': uuid,
                    'course': course
                }
            })
       
@app.route('/profile', methods=['POST', 'GET'])
def profile() -> str:
    # link http://localhost:8080/profile?uuid=30863
    
    # gets the user's profile data based on the uuid and returns it as a json object
    
    usr = request.args.get('uuid')
    
    try:
        conn = sqlite3.connect('src/database/users.db')
        c = conn.cursor()
        
        # fetch the user's data from the database
        data = c.execute("SELECT * FROM users WHERE Uuid = ?", (usr,)).fetchone()
        
        courses = data[5].split(",")[:-1]
        
        # return a json object that has status code and the data added to the database
        return jsonify({
            'status': 200, 
            'info':'ok' ,'data': 
                {
                    'uuid': data[0], 
                    'username': data[1], 
                    'email': data[2], 
                    'password': data[3], 
                    'pfp': data[4], 
                    'courses': courses
                }
            })
    
    except:
        # just in case something goes wrong
        return jsonify({
            'status': 400, 
            'info':'err' ,'data': 
                {
                    'uuid': 'null', 
                    'username': 'null', 
                    'email': 'null', 
                    'password': 'null', 
                    'pfp': 'null', 
                    'courses': 'null'
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
    
    conn=sqlite3.connect('src/database/users.db')
    c=conn.cursor()
    
    c.execute("INSERT INTO courses VALUES (?, ?, ?, ?)", ((title + ","), float(price), author, int(rating)))
    conn.commit()
    conn.close()
    
    # return a json object that has status code and the data added to the database
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
        
@app.route('/getcourse', methods=['POST', 'GET'])
def getcourse() -> str:
    # link: http://localhost:8080/getcourse
    
    # returns all the courses in the database

    try:
        conn=sqlite3.connect('src/database/users.db')
        c=conn.cursor()
        cur = c.execute("SELECT * FROM courses").fetchall()
        conn.close()
        
        # return a json object that has status code and the data added to the database
        return jsonify({
            'status': 200,
            'info': 'ok',
            'data': cur
        })

    except:
        # just in case something goes wrong
        return jsonify({
            'status': 400,
            'info': 'err',
            'data': None
        })
    
    
    
        

if __name__ == '__main__':
    app.run(port = 8080)