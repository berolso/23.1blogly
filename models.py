"""Models for Blogly."""
 
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

def connect_db(app):
  '''connect to db'''
  db.app = app
  db.init_app(app)

class User(db.Model):

  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  first_name = db.Column(db.String(30), nullable=False)
  last_name = db.Column(db.String, nullable=False)
  image_url = db.Column(db.String, default='https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSezD4QP_WuZR9_mTWxGPHcnB9NdjLwYJ43iA&usqp=CAU')

  @property
  def full_name(self):
    return f'{self.first_name} {self.last_name}'

