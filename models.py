"""Models for Blogly."""
 
from flask_sqlalchemy import SQLAlchemy 
from datetime import date as dt

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

  posts = db.relationship('Post', backref='user',cascade="all, delete-orphan")

  @property
  def full_name(self):
    return f'{self.first_name} {self.last_name}'

  def __repr__(self):
	  return f'<User | {self.id} | {self.full_name} | {self.posts}>'

class Post(db.Model):

  __tablename__ = 'posts'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title = db.Column(db.String, nullable=False)
  content = db.Column(db.Text, nullable=False)
  created_at = db.Column(db.Date, nullable=False,default=dt.today())
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False) 

  tags = db.relationship('Tag', secondary='post_tags', backref='posts')

  post_tags = db.relationship('PostTag', backref='post', cascade="all, delete-orphan")

  @property
  def friendly_date(self):
    """Return nicely-formatted date."""
    return self.created_at.strftime("%a %b %-d %Y")

  def __repr__(self):
	  return f'<Post | {self.id} | {self.title} | {self.created_at}>'


class Tag(db.Model):

  __tablename__ = 'tags'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String, nullable=False, unique=True)

  # post_tags = db.relationship('PostTag', backref='tag',cascade="all, delete-orphan")

  def __repr__(self):
    return f'<Tag {self.id} | {self.name}>'

class PostTag(db.Model):

  __tablename__ = 'post_tags'

  post_id = db.Column(db.Integer, db.ForeignKey('posts.id'),primary_key=True,)
  tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)