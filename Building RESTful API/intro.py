# Building RESTful APIs with Flask

# What is a RESTful API?
'''
    A RESTful API is an API that follows the principles of REST (Representational State Transfer). 
    It allows communication between a client and server using standard HTTP methods like GET, POST, PUT, and DELETE.
'''

# What is Flask?
'''
    Flask is a lightweight, micro web framework for Python that allows developers to build web applications and APIs quickly. 
    Flask is highly flexible and simple to set up, making it popular for small to medium-sized projects and APIs.
'''

# 1. Virtual Environment Setup
# create virtual env: "python3 -m venv venv"
# activate virtual env: "venv\Scripts\activate"(windows) "source venv/bin/activate"(mac)

# 2. Install Flask and Flask-Marshmallow: "pip install Flask Flask-Marshmallow marshmallow-sqlalchemy"

# 3. Basic Flask Application

# import flask
from flask import Flask

# create an instance of the Flask Class
app = Flask(__name__)

# at this route, the respective function gets called.
# NOTE: the .route() method, by default, is a GET request. To allow other http methods, you can pass the additional arguement = "methods=["GET", "POST"]"
@app.route('/home')
def home():
    return 'Welcome to the Flask REST API'

# run the flask server with the command: "flask run" (flask defaults to "app.py" to find the flask instance). Otherwise, "flask --app <file-name> run"