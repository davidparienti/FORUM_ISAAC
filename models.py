from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forums.db'
db = SQLAlchemy(app)


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.Text,unique=True)
  password = db.Column(db.Text)


class Discussion(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.Text)


class Message(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.Text)
  date = db.Column(db.DateTime, default=datetime.datetime.now)
  discussion_id = db.Column(db.Integer, db.ForeignKey('discussion.id'), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  







