"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def home():
  return redirect('/users')

@app.route('/users')
def list_users():
  # order users list by last and first name
  users = User.query.order_by(User.last_name, User.first_name).all()
  # users = User.query.all()
  return render_template('index.html', users=users)

@app.route('/users/new')
def add_new_user():
  return render_template('new.html')

@app.route('/users/new', methods=['POST'])
def create_new_user():
  new_user = User(
  first_name=request.form['first'],
  last_name=request.form['last'],
  image_url=request.form['image']
  )
  db.session.add(new_user)
  db.session.commit()
  return redirect('/users')

@app.route('/users/<int:user_id>')
def user_detail(user_id):
  user = User.query.get_or_404(user_id)
  return render_template('user.html', user=user)

@app.route('/users/<int:user_id>/edit')
def get_edit_user(user_id):
  user = User.query.get_or_404(user_id)
  return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def post_edit_user(user_id):
  user = User.query.get_or_404(user_id)
  user.first_name = request.form['first']
  user.last_name = request.form['last']
  user.image_url = request.form['image']
  db.session.add(user)
  db.session.commit()
  return redirect(f'/users/{user.id}')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
  user = User.query.get_or_404(user_id)
  db.session.delete(user)
  db.session.commit()
  return redirect('/users')


