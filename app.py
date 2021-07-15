"""Blogly application"""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post, DEFAULT_URL
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    """Redirect to the list of users"""
    return redirect('/users')

@app.route('/users')
def show_users():
    """Show all users"""
    users = User.query.all()
    return render_template('users.html', users = users)


@app.route('/users/new')
def show_add_form():
    """Show an add form for users"""
    return render_template('newuser.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    """Process the add form, adding a new user and going back to the list of users"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_info(user_id):
    """Show information about the given user"""

    user = User.query.get_or_404(user_id)
    return render_template('userinfo.html',user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user_info(user_id):
    """Show the edit page for a user"""

    user = User.query.get_or_404(user_id)
    return render_template('useredit.html',user=user)

@app.route('/users/<int:user_id>/edit',methods=["POST"])
def save_user_edit(user_id):
    """Process the edit form, return the user to the list of users"""

    user = User.query.get_or_404(user_id)
    
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url'] or DEFAULT_URL

    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete',methods=["POST"])
def delete_user(user_id):
    """Delete the user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def show_add_post_form(user_id):
    """Show an add form for post"""

    user = User.query.get_or_404(user_id)
    return render_template('newpost.html',user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """Process the add form, adding a new post and going back to user info page"""
    title = request.form['title']
    content = request.form['content']

    post = Post(title=title, content=content, user_id=user_id)
    
    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')
