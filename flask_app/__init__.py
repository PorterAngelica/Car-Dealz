from flask import Flask
from flask_bcrypt import Bcrypt        
app = Flask(__name__)
app.secret_key = "mysecretshh"
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 