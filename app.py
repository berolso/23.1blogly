"""Blogly application."""

from flask import Flask, request, redirect, render_template, url_for, flash
from models import db, connect_db, User, Post

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

# custom 404
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

# index
@app.route('/')
def home():
  return redirect('/posts')

# ----- user routes -----

@app.route('/users')
def list_users():
  '''all users list'''
  # order users list by last and first name
  users = User.query.order_by(User.last_name, User.first_name).all()
  # users = User.query.all()
  return render_template('users.html', users=users)

@app.route('/users/new')
def create_new_user():
  '''create new user page'''
  return render_template('new_user.html')

@app.route('/users/new', methods=['POST'])
def post_new_user():
  '''POST new user'''
  new_user = User(
  first_name=request.form['first'],
  last_name=request.form['last'],
  image_url=request.form['image']
  )
  db.session.add(new_user)
  db.session.commit()
  flash("User successfully added", "success")
  return redirect('/users')

@app.route('/users/<int:user_id>')
def user_detail(user_id):
  '''user page'''
  user = User.query.get_or_404(user_id)
  return render_template('user.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
  '''edit user page'''
  user = User.query.get_or_404(user_id)
  return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def post_edit_user(user_id):
  '''POST edit user'''
  user = User.query.get_or_404(user_id)
  user.first_name = request.form['first']
  user.last_name = request.form['last']
  user.image_url = request.form['image']
  db.session.add(user)
  db.session.commit()
  flash("User successfully Edited", "secondary")
  return redirect(f'/users/{user.id}')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def post_delete_user(user_id):
  '''delete user'''
  user = User.query.get_or_404(user_id)
  db.session.delete(user)
  db.session.commit()
  flash("User successfully Deleted", "danger")
  return redirect('/users')


  # ----- user posts routes -----

@app.route('/posts')
def list_posts():
  '''list 5 posts'''
  # get 5 last posts ordered by created date
  posts = Post.query.order_by(Post.created_at, Post.title).limit(5) 
  return render_template('posts.html', posts=posts)  

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
  '''new post page'''
  user = User.query.get_or_404(user_id)
  return render_template('new_post.html',user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def post_new_post(user_id):
  '''POST new post'''
  user = User.query.get_or_404(user_id)
  new_post = Post(
    title = request.form['title'],
    content = request.form['content'],
    user_id = user.id
  )
  db.session.add(new_post)
  db.session.commit()
  flash("Post successfully Added", "success")
  return redirect(url_for('user_detail',user_id=user_id))


@app.route('/posts/<int:post_id>')
def post_page(post_id):
  '''post page'''
  post = Post.query.get_or_404(post_id)
  return render_template('post.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
  '''edit post page'''
  post = Post.query.get_or_404(post_id)
  return render_template('edit_post.html', post=post)

@app.route('/posts/<int:post_id>/edit',methods=['POST'])
def post_edit_post(post_id):
  '''POST post edits'''
  post = Post.query.get_or_404(post_id)
  post.title = request.form['title']
  post.content = request.form['content']
  db.session.add(post)
  db.session.commit()
  flash("Post successfully Edited", "secondary")
  return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>/delete',methods=['POST'])
def post_delete_post(post_id):
  '''delete post'''
  post = Post.query.get_or_404(post_id)
  db.session.delete(post)
  db.session.commit()
  flash("Post successfully Deleted", "danger")
  return redirect(f'/users/{post.user_id}')
