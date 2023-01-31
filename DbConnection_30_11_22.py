from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:root@localhost:5432/LibraryManagementSystem"
app.config['SECRET_KEY'] = 'secret'
db = SQLAlchemy(app)
