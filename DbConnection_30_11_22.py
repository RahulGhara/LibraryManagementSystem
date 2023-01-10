from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:root@localhost:5432/LibraryManagementSystem"
app.config['SECRET_KEY'] = 'secret'
db = SQLAlchemy(app)
key = Fernet.generate_key()
fernet = Fernet(key)
