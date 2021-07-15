"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User
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
    return redirect('/users')

@app.route('/users')
def show_users():

    users = User.query.all()
    return render_template('users.html', users = users)


@app.route('/users/new')
def show_add_form():

    return render_template('newuser.html')

@app.route('/users/new', methods=["POST"])
def add_user():

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    # Maybe enforce 50 characters later (add validation on the form)

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_info(user_id):

    user = User.query.get_or_404(user_id)
    return render_template('userinfo.html',user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user_info(user_id):

    user = User.query.get_or_404(user_id)
    return render_template('useredit.html',user=user)

@app.route('/users/<int:user_id>/edit',methods=["POST"])
def save_user_edit(user_id):

    user = User.query.get_or_404(user_id)
    
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
# combine this with above lines
    user.first_name = first_name
    user.last_name = last_name

    # if empty string, pass in Null... so this will trigger the default
    user.image_url = image_url

    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete',methods=["POST"])
def delete_user(user_id):

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')
